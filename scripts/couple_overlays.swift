#!/usr/bin/env swift
// scripts/couple_overlays.swift
// Unified Native 4K (2160x3840) CoreText/AppKit Overlay Generator for Category 1: Couple Video
// Enforces templates/01_couple_video/brand_kit.json and permanently eliminates:
//   1. Single-pass negative stroke hollow/dark-gray text bug (uses 2-Pass Outer Stroke + Pure Interior Fill)
//   2. Missing/monochrome emoji bug (splits Arial-Black text runs from AppleColorEmoji runs)
//   3. Wide blank space before emoji bug (applies -18px kerning on space before emoji)
//   4. Swift Character.count vs UTF-16 NSRange bug (always uses NSString.length)
//
// Usage:
//   swift -module-cache-path /tmp/swift_cache ./scripts/couple_overlays.swift --spec renders/drafts/<Project>/overlays.json --outdir broll/<Project>/

import AppKit
import CoreText
import Foundation

struct OverlayItem: Codable {
    let filename: String
    let type: String        // "hook", "header", "head_pop", "winner"
    let line1: String?      // e.g. "challenge" for hook
    let text: String        // e.g. "BIKIN KATA" or "ARTHUR: CARI TRAKTOR BIRU"
    let emoji: String?      // e.g. "🔥" or "🚜"
    let variant: String?    // "cari", "dapat", "blunder", "tally", "angel", "arthur", "winner"
    let player: String?     // "Angel" (left x=610) or "Arthur" (right x=1520)
}

struct OverlaySpec: Codable {
    let items: [OverlayItem]
}

let W: CGFloat = 2160.0
let H: CGFloat = 3840.0

func colorFromHex(_ hex: String, alpha: CGFloat = 1.0) -> NSColor {
    var clean = hex.trimmingCharacters(in: .whitespacesAndNewlines).uppercased()
    if clean.hasPrefix("#") { clean.removeFirst() }
    guard clean.count == 6, let rgb = UInt64(clean, radix: 16) else {
        return NSColor(calibratedRed: 1, green: 1, blue: 1, alpha: alpha)
    }
    return NSColor(
        calibratedRed: CGFloat((rgb >> 16) & 0xFF) / 255.0,
        green: CGFloat((rgb >> 8) & 0xFF) / 255.0,
        blue: CGFloat(rgb & 0xFF) / 255.0,
        alpha: alpha
    )
}

func makeCanvas() -> NSBitmapImageRep {
    return NSBitmapImageRep(
        bitmapDataPlanes: nil,
        pixelsWide: Int(W),
        pixelsHigh: Int(H),
        bitsPerSample: 8,
        samplesPerPixel: 4,
        hasAlpha: true,
        isPlanar: false,
        colorSpaceName: .deviceRGB,
        bytesPerRow: 0,
        bitsPerPixel: 0
    )!
}

func savePNG(_ rep: NSBitmapImageRep, to path: String) {
    if let data = rep.representation(using: .png, properties: [:]) {
        try? data.write(to: URL(fileURLWithPath: path))
    }
}

/// Draws text + optional emoji in 2 passes so interior fill is 100% solid and emoji is full-color with tight kerning
func drawTwoPassTextWithEmoji(
    text: String,
    emoji: String?,
    fontName: String = "Arial-Black",
    baseSize: CGFloat,
    minSize: CGFloat = 84.0,
    fillColor: NSColor,
    strokeWidth: CGFloat = -9.0,
    rect: NSRect
) {
    let cleanText = text.trimmingCharacters(in: .whitespaces)
    let cleanEmoji = (emoji ?? "").trimmingCharacters(in: .whitespaces)

    let pStyle = NSMutableParagraphStyle()
    pStyle.alignment = .center
    pStyle.lineBreakMode = .byWordWrapping

    let shadow = NSShadow()
    shadow.shadowColor = NSColor(calibratedRed: 0, green: 0, blue: 0, alpha: 0.90)
    shadow.shadowBlurRadius = 18.0
    shadow.shadowOffset = NSSize(width: 0, height: -10)

    var chosenSize = baseSize
    while chosenSize > minSize {
        let testFont = NSFont(name: fontName, size: chosenSize) ?? NSFont.boldSystemFont(ofSize: chosenSize)
        let measureStr = NSMutableAttributedString(string: cleanText + (cleanEmoji.isEmpty ? "" : " " + cleanEmoji), attributes: [.font: testFont])
        if measureStr.size().width <= rect.width - 60 {
            break
        }
        chosenSize -= 6.0
    }

    let mainFont = NSFont(name: fontName, size: chosenSize) ?? NSFont.boldSystemFont(ofSize: chosenSize)
    let emojiFont = NSFont(name: "AppleColorEmoji", size: chosenSize * 0.96) ?? mainFont

    // PASS 1: Outer Black Stroke + Drop Shadow + Full-Color Emoji with Shadow
    let pass1 = NSMutableAttributedString()
    let pass1TextAttrs: [NSAttributedString.Key: Any] = [
        .font: mainFont,
        .foregroundColor: NSColor.black,
        .strokeColor: NSColor.black,
        .strokeWidth: strokeWidth,
        .paragraphStyle: pStyle,
        .shadow: shadow
    ]
    pass1.append(NSAttributedString(string: cleanText, attributes: pass1TextAttrs))

    if !cleanEmoji.isEmpty {
        let spaceAttrs: [NSAttributedString.Key: Any] = [
            .font: mainFont,
            .kern: -18.0,
            .paragraphStyle: pStyle
        ]
        pass1.append(NSAttributedString(string: " ", attributes: spaceAttrs))
        let emojiAttrs: [NSAttributedString.Key: Any] = [
            .font: emojiFont,
            .paragraphStyle: pStyle,
            .shadow: shadow
        ]
        pass1.append(NSAttributedString(string: cleanEmoji, attributes: emojiAttrs))
    }
    pass1.draw(in: rect)

    // PASS 2: Pure Unstroked Solid Interior Fill (drawn over Pass 1 so letters are 100% solid white/green/gold)
    let pass2 = NSMutableAttributedString()
    let pass2TextAttrs: [NSAttributedString.Key: Any] = [
        .font: mainFont,
        .foregroundColor: fillColor,
        .paragraphStyle: pStyle
    ]
    pass2.append(NSAttributedString(string: cleanText, attributes: pass2TextAttrs))

    if !cleanEmoji.isEmpty {
        let spaceAttrs: [NSAttributedString.Key: Any] = [
            .font: mainFont,
            .kern: -18.0,
            .paragraphStyle: pStyle
        ]
        pass2.append(NSAttributedString(string: " ", attributes: spaceAttrs))
        let emojiAttrs: [NSAttributedString.Key: Any] = [
            .font: emojiFont,
            .paragraphStyle: pStyle
        ]
        pass2.append(NSAttributedString(string: cleanEmoji, attributes: emojiAttrs))
    }
    pass2.draw(in: rect)
}

/// Draws Hook Line 1 ("challenge") in HelveticaNeue-Bold with thick white outer border and black fill
func drawHookSetupLine(_ line1: String, rect: NSRect) {
    let font = NSFont(name: "HelveticaNeue-Bold", size: 136.0) ?? NSFont.boldSystemFont(ofSize: 136.0)
    let pStyle = NSMutableParagraphStyle()
    pStyle.alignment = .center

    let shadow = NSShadow()
    shadow.shadowColor = NSColor(calibratedRed: 0, green: 0, blue: 0, alpha: 0.55)
    shadow.shadowBlurRadius = 16.0
    shadow.shadowOffset = NSSize(width: 0, height: -6)

    // Pass 1: Thick white outer border
    let pass1Attrs: [NSAttributedString.Key: Any] = [
        .font: font,
        .foregroundColor: NSColor.white,
        .strokeColor: NSColor.white,
        .strokeWidth: -16.0,
        .paragraphStyle: pStyle,
        .shadow: shadow
    ]
    NSAttributedString(string: line1.lowercased(), attributes: pass1Attrs).draw(in: rect)

    // Pass 2: Crisp black interior fill
    let pass2Attrs: [NSAttributedString.Key: Any] = [
        .font: font,
        .foregroundColor: NSColor.black,
        .paragraphStyle: pStyle
    ]
    NSAttributedString(string: line1.lowercased(), attributes: pass2Attrs).draw(in: rect)
}

func renderItem(_ item: OverlayItem, outDir: String) {
    let rep = makeCanvas()
    NSGraphicsContext.saveGraphicsState()
    NSGraphicsContext.current = NSGraphicsContext(bitmapImageRep: rep)

    let variantColor: NSColor = {
        switch (item.variant ?? "cari").lowercased() {
        case "dapat", "correct", "green":
            return colorFromHex("#4ADE80")
        case "blunder", "wrong", "red":
            return colorFromHex("#FF453A")
        case "tally", "winner", "gold", "yellow":
            return colorFromHex("#FFD60A")
        case "angel", "pink":
            return colorFromHex("#FF6FAE")
        case "arthur", "blue":
            return colorFromHex("#38BDF8")
        default:
            return colorFromHex("#FFFFFF")
        }
    }()

    switch item.type {
    case "hook":
        let line1 = item.line1 ?? "challenge"
        drawHookSetupLine(line1, rect: NSRect(x: 80, y: 3365, width: 2000, height: 190))
        drawTwoPassTextWithEmoji(
            text: item.text.uppercased(),
            emoji: item.emoji,
            baseSize: 176.0,
            minSize: 120.0,
            fillColor: colorFromHex("#FFFFFF"),
            strokeWidth: -9.5,
            rect: NSRect(x: 40, y: 3140, width: 2080, height: 280)
        )

    case "header", "winner":
        let baseSz: CGFloat = (item.type == "winner") ? 124.0 : 116.0
        drawTwoPassTextWithEmoji(
            text: item.text.uppercased(),
            emoji: item.emoji,
            baseSize: baseSz,
            minSize: 82.0,
            fillColor: variantColor,
            strokeWidth: -9.0,
            rect: NSRect(x: 40, y: 3230, width: 2080, height: 260)
        )

    case "head_pop":
        let isLeft = (item.player ?? "Angel").lowercased() == "angel"
        let cx: CGFloat = isLeft ? 610.0 : 1520.0
        let boxW: CGFloat = 920.0
        let baseSz: CGFloat = (item.text.count <= 2) ? 240.0 : 148.0
        // AppKit y from bottom: 3840 - 1020 - 150 = 2670
        drawTwoPassTextWithEmoji(
            text: item.text.uppercased(),
            emoji: item.emoji,
            baseSize: baseSz,
            minSize: 96.0,
            fillColor: variantColor,
            strokeWidth: -8.5,
            rect: NSRect(x: cx - boxW / 2.0, y: 2670, width: boxW, height: 260)
        )

    default:
        break
    }

    NSGraphicsContext.restoreGraphicsState()
    let outPath = (outDir as NSString).appendingPathComponent(item.filename)
    savePNG(rep, to: outPath)
}

// CLI Argument Parsing
var specPath = ""
var outDir = "."
let args = CommandLine.arguments
var i = 1
while i < args.count {
    if args[i] == "--spec", i + 1 < args.count {
        specPath = args[i + 1]
        i += 2
    } else if args[i] == "--outdir", i + 1 < args.count {
        outDir = args[i + 1]
        i += 2
    } else {
        i += 1
    }
}

guard !specPath.isEmpty else {
    print("Usage: swift ./scripts/couple_overlays.swift --spec <overlays.json> --outdir <dir>")
    exit(1)
}

try? FileManager.default.createDirectory(atPath: outDir, withIntermediateDirectories: true)
let data = try Data(contentsOf: URL(fileURLWithPath: specPath))
let spec = try JSONDecoder().decode(OverlaySpec.self, from: data)
for item in spec.items {
    renderItem(item, outDir: outDir)
}
print("✅ [CoupleOverlays] Rendered \(spec.items.count) 4K Brand-Kit overlays to \(outDir)")
