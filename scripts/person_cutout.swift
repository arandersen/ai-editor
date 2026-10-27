#!/usr/bin/env swift
// scripts/person_cutout.swift
// Hardware-accelerated macOS Apple Vision Person Segmentation (VNGeneratePersonSegmentationRequest)
// Extracts a [start, end] clip from a source video and outputs a feathered ProRes 4444 (.mov)
// foreground alpha matte for @text-behind-head and @magazine-cover effects.
//
// Usage:
//   swift ./scripts/person_cutout.swift --input raw/clip.mp4 --start 0.0 --end 4.0 --output broll/cutout.mov

import Foundation
import AVFoundation
import Vision
import CoreImage

var inputPath = ""
var outputPath = ""
var startSec: Double = 0.0
var endSec: Double = 5.0

let args = CommandLine.arguments
var i = 1
while i < args.count {
    switch args[i] {
    case "--input":
        i += 1; if i < args.count { inputPath = args[i] }
    case "--output":
        i += 1; if i < args.count { outputPath = args[i] }
    case "--start":
        i += 1; if i < args.count { startSec = Double(args[i]) ?? 0.0 }
    case "--end":
        i += 1; if i < args.count { endSec = Double(args[i]) ?? 5.0 }
    default:
        break
    }
    i += 1
}

if inputPath.isEmpty || outputPath.isEmpty {
    print("Usage: swift scripts/person_cutout.swift --input <video.mp4> --start <sec> --end <sec> --output <cutout.mov>")
    exit(1)
}

let inputURL = URL(fileURLWithPath: inputPath)
let outputURL = URL(fileURLWithPath: outputPath)
try? FileManager.default.removeItem(at: outputURL)
try? FileManager.default.createDirectory(at: outputURL.deletingLastPathComponent(), withIntermediateDirectories: true)

let asset = AVURLAsset(url: inputURL)
guard let videoTrack = asset.tracks(withMediaType: .video).first else {
    print("❌ No video track found in \(inputPath)")
    exit(1)
}

let naturalSize = videoTrack.naturalSize.applying(videoTrack.preferredTransform)
let width = Int(abs(naturalSize.width))
let height = Int(abs(naturalSize.height))

let reader = try! AVAssetReader(asset: asset)
let startCM = CMTime(seconds: startSec, preferredTimescale: 600)
let durCM = CMTime(seconds: max(0.1, endSec - startSec), preferredTimescale: 600)
reader.timeRange = CMTimeRange(start: startCM, duration: durCM)

let readerSettings: [String: Any] = [
    kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_32BGRA
]
let trackOutput = AVAssetReaderTrackOutput(track: videoTrack, outputSettings: readerSettings)
trackOutput.alwaysCopiesSampleData = false
reader.add(trackOutput)

let writer = try! AVAssetWriter(outputURL: outputURL, fileType: .mov)
let writerSettings: [String: Any] = [
    AVVideoCodecKey: AVVideoCodecType.proRes4444,
    AVVideoWidthKey: width,
    AVVideoHeightKey: height
]
let writerInput = AVAssetWriterInput(mediaType: .video, outputSettings: writerSettings)
writerInput.expectsMediaDataInRealTime = false
let adaptorAttrs: [String: Any] = [
    kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_32BGRA,
    kCVPixelBufferWidthKey as String: width,
    kCVPixelBufferHeightKey as String: height
]
let adaptor = AVAssetWriterInputPixelBufferAdaptor(assetWriterInput: writerInput, sourcePixelBufferAttributes: adaptorAttrs)
writer.add(writerInput)

let ciContext = CIContext(options: [.useSoftwareRenderer: false])
let segRequest = VNGeneratePersonSegmentationRequest()
segRequest.qualityLevel = .accurate
segRequest.outputPixelFormat = kCVPixelFormatType_OneComponent8

reader.startReading()
writer.startWriting()
writer.startSession(atSourceTime: .zero)

var frameCount = 0
print("✂️ [PersonCutout] Segmenting person via Apple Vision ANE (\(width)x\(height), \(startSec)s -> \(endSec)s)...")

while reader.status == .reading {
    autoreleasepool {
        guard let sampleBuffer = trackOutput.copyNextSampleBuffer(),
              let imageBuffer = CMSampleBufferGetImageBuffer(sampleBuffer) else {
            return
        }
        let pts = CMSampleBufferGetPresentationTimeStamp(sampleBuffer) - startCM
        let handler = VNImageRequestHandler(cvPixelBuffer: imageBuffer, options: [:])
        try? handler.perform([segRequest])

        let origCI = CIImage(cvPixelBuffer: imageBuffer)
        var outCI = origCI

        if let maskBuffer = segRequest.results?.first?.pixelBuffer {
            var maskCI = CIImage(cvPixelBuffer: maskBuffer)
            let scaleX = origCI.extent.width / maskCI.extent.width
            let scaleY = origCI.extent.height / maskCI.extent.height
            maskCI = maskCI.transformed(by: CGAffineTransform(scaleX: scaleX, y: scaleY))
                           .applyingFilter("CIGaussianBlur", parameters: [kCIInputRadiusKey: 1.5])
                           .cropped(to: origCI.extent)

            let clearBG = CIImage.empty().cropped(to: origCI.extent)
            if let blend = CIFilter(name: "CIBlendWithMask", parameters: [
                kCIInputImageKey: origCI,
                kCIInputBackgroundImageKey: clearBG,
                kCIInputMaskImageKey: maskCI
            ])?.outputImage {
                outCI = blend
            }
        }

        var outPixelBuffer: CVPixelBuffer?
        CVPixelBufferPoolCreatePixelBuffer(nil, adaptor.pixelBufferPool!, &outPixelBuffer)
        if let dst = outPixelBuffer {
            ciContext.render(outCI, to: dst)
            while !writerInput.isReadyForMoreMediaData {
                Thread.sleep(forTimeInterval: 0.002)
            }
            adaptor.append(dst, withPresentationTime: pts)
            frameCount += 1
        }
    }
}

writerInput.markAsFinished()
let sema = DispatchSemaphore(value: 0)
writer.finishWriting {
    sema.signal()
}
sema.wait()
print("✅ [PersonCutout] Exported \(frameCount) frames to ProRes 4444 alpha matte: \(outputPath)")
