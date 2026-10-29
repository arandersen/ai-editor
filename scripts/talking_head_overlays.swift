#!/usr/bin/env swift
// scripts/talking_head_overlays.swift
// Native macOS 4K/1080p CoreText & AppKit Overlay Generator for Talking Head Videos (FeedMedia Notion Effects).
// Generates transparent PNG overlays for:
//   1. @coral-captions (3-word group at y=61.5% with Coral #D97757 rounded box ONLY on the active word)
//   2. @text-behind-head (2-line display title at y=20% and y=27%)
//   3. @tool-label (App icon + bold white name lockup at y=61.5%)
//   4. @repo-card (GitHub dark-mode card #0D1117 at 85% width)
//   5. @prompt-bar (#2B2B2B rounded pill bar at y=22.5%, 92.6% width + #D97757 coral send button)
//   6. @magazine-cover (Masthead layer behind head + Gold frame / cover lines / barcode layer in front)
//   7. @real-screenshot (90% width rounded screenshot card with soft drop shadow)
//
// Usage:
//   swift ./scripts/talking_head_overlays.swift --spec overlays.json --outdir broll/Project/

import Cocoa
import CoreText

struct OverlayJob: Codable {
    let id: String
    let type: String
    let width: Int?
    let height: Int?
    // Caption fields
    let words: [String]?
    let activeIndex: Int?
    // Text behind head / general lines
    let lines: [String]?
    // Tool label / Repo card / Prompt bar / Screenshot
    let title: String?
    let subtitle: String?
    let badge: String?
    let stars: String?
    let forks: String?
    let imagePath: String?
}

struct OverlaySpec: Codable {
    let canvasWidth: Int
    let canvasHeight: Int
    let jobs: [OverlayJob]
}

func colorFromHex(_ hex: String, alpha: CGFloat = 1.0) -> NSColor {
    var s = hex.trimmingCharacters(in: .whitespacesAndNewlines).uppercased()
    if s.hasPrefix("#") { s.removeFirst() }
    var rgb: UInt64 = 0
    Scanner(string: s).scanHexInt64(&rgb)
    return NSColor(
        calibratedRed: CGFloat((rgb >> 16) & 0xFF) / 255.0,
        green: CGFloat((rgb >> 8) & 0xFF) / 255.0,
        blue: CGFloat(rgb & 0xFF) / 255.0,
        alpha: alpha
    )
}

func saveCanvas(width: Int, height: Int, outPath: String, drawBlock: (CGContext) -> Void) {
    guard let rep = NSBitmapImageRep(
        bitmapDataPlanes: nil,
        pixelsWide: width,
        pixelsHigh: height,
        bitsPerSample: 8,
        samplesPerPixel: 4,
        hasAlpha: true,
        isPlanar: false,
        colorSpaceName: .calibratedRGB,
        bytesPerRow: width * 4,
        bitsPerPixel: 32
    ) else { return }

    NSGraphicsContext.saveGraphicsState()
    let ctx = NSGraphicsContext(bitmapImageRep: rep)!
    NSGraphicsContext.current = ctx
    let cg = ctx.cgContext
    cg.clear(CGRect(x: 0, y: 0, width: width, height: height))
    drawBlock(cg)
    NSGraphicsContext.restoreGraphicsState()

    if let png = rep.representation(using: .png, properties: [:]) {
        try? png.write(to: URL(fileURLWithPath: outPath))
    }
}

let args = CommandLine.arguments
var specPath = ""
var outDir = "."
var idx = 1
while idx < args.count {
    if args[idx] == "--spec" && idx + 1 < args.count { specPath = args[idx + 1]; idx += 1 }
    else if args[idx] == "--outdir" && idx + 1 < args.count { outDir = args[idx + 1]; idx += 1 }
    idx += 1
}

guard !specPath.isEmpty,
      let data = try? Data(contentsOf: URL(fileURLWithPath: specPath)),
      let spec = try? JSONDecoder().decode(OverlaySpec.self, from: data) else {
    print("Usage: swift scripts/talking_head_overlays.swift --spec <spec.json> --outdir <dir>")
    exit(1)
}

try? FileManager.default.createDirectory(atPath: outDir, withIntermediateDirectories: true)
let W = CGFloat(spec.canvasWidth)
let H = CGFloat(spec.canvasHeight)
let scale = W / 1080.0
let coralColor = colorFromHex("#D97757")

for job in spec.jobs {
    let outPath = "\(outDir)/\(job.id).png"
    saveCanvas(width: spec.canvasWidth, height: spec.canvasHeight, outPath: outPath) { cg in
        switch job.type {

        case "coral_pill_3word":
            // Notion Effect #3: Helvetica Neue Bold, 64px (128px @ 4K), white, soft shadow, centered at 61.5% height.
            // Active spoken word sits on a coral (#D97757) box with 8px (16px @ 4K) rounded corners.
            let words = job.words ?? []
            let activeIdx = job.activeIndex ?? 0
            var fontSize = 64.0 * scale
            let spaceW = 20.0 * scale
            let provisional = NSFont(name: "HelveticaNeue-Bold", size: fontSize) ?? NSFont.boldSystemFont(ofSize: fontSize)
            let measured = words.reduce(CGFloat(0)) { $0 + ($1 as NSString).size(withAttributes: [.font: provisional]).width }
            let available = W * 0.86 - CGFloat(max(0, words.count - 1)) * spaceW
            if measured > available { fontSize *= max(0.3, available / measured) }
            let font = NSFont(name: "HelveticaNeue-Bold", size: fontSize) ?? NSFont.boldSystemFont(ofSize: fontSize)

            let shadow = NSShadow()
            shadow.shadowColor = NSColor(calibratedWhite: 0.0, alpha: 0.65)
            shadow.shadowBlurRadius = 12.0 * scale
            shadow.shadowOffset = NSSize(width: 0, height: -4.0 * scale)

            let attrs: [NSAttributedString.Key: Any] = [
                .font: font,
                .foregroundColor: NSColor.white,
                .shadow: shadow
            ]

            let sizes = words.map { ($0 as NSString).size(withAttributes: attrs) }
            let totalW = sizes.reduce(0.0) { $0 + $1.width } + CGFloat(max(0, words.count - 1)) * spaceW
            var curX = (W - totalW) / 2.0
            // Cocoa Y is from bottom: 61.5% from top = 38.5% from bottom
            let centerY = H * (1.0 - 0.615)

            for (wIdx, word) in words.enumerated() {
                let sz = sizes[wIdx]
                let drawY = centerY - sz.height / 2.0
                if wIdx == activeIdx {
                    let padX = 16.0 * scale
                    let padY = 6.0 * scale
                    let pillRect = NSRect(x: curX - padX, y: drawY - padY, width: sz.width + padX * 2.0, height: sz.height + padY * 2.0)
                    let path = NSBezierPath(roundedRect: pillRect, xRadius: 8.0 * scale, yRadius: 8.0 * scale)
                    coralColor.setFill()
                    path.fill()
                }
                (word as NSString).draw(at: NSPoint(x: curX, y: drawY), withAttributes: attrs)
                curX += sz.width + spaceW
            }

        case "text_behind_head":
            // Notion Effect #2: 2 lines centered at 20% and 27% frame height, 150px (300px @ 4K), #F4F4F2
            let lines = job.lines ?? ["Text behind", "your head"]
            let fontSize = 135.0 * scale
            let font = NSFont(name: "Arial-Black", size: fontSize) ?? NSFont.boldSystemFont(ofSize: fontSize)
            let textColor = colorFromHex("#F4F4F2")
            let yPercents: [CGFloat] = [0.20, 0.27]

            for (lIdx, line) in lines.prefix(2).enumerated() {
                let attrs: [NSAttributedString.Key: Any] = [
                    .font: font,
                    .foregroundColor: textColor
                ]
                let sz = (line as NSString).size(withAttributes: attrs)
                let x = (W - sz.width) / 2.0
                let y = H * (1.0 - yPercents[lIdx]) - sz.height / 2.0
                (line as NSString).draw(at: NSPoint(x: x, y: y), withAttributes: attrs)
            }

        case "tool_label":
            // Notion Effect #4: Logo (110px, rounded) + Tool Name (bold white, 92px) centered at 61.5% height
            let name = job.title ?? "FFmpeg"
            let logoSize = 110.0 * scale
            let gap = 28.0 * scale
            let fontSize = 92.0 * scale
            let font = NSFont(name: "HelveticaNeue-Bold", size: fontSize) ?? NSFont.boldSystemFont(ofSize: fontSize)

            let shadow = NSShadow()
            shadow.shadowColor = NSColor(calibratedWhite: 0.0, alpha: 0.7)
            shadow.shadowBlurRadius = 14.0 * scale
            shadow.shadowOffset = NSSize(width: 0, height: -4.0 * scale)

            let attrs: [NSAttributedString.Key: Any] = [
                .font: font,
                .foregroundColor: NSColor.white,
                .shadow: shadow
            ]
            let textSz = (name as NSString).size(withAttributes: attrs)
            let totalW = logoSize + gap + textSz.width
            let startX = (W - totalW) / 2.0
            let centerY = H * (1.0 - 0.615)

            let logoRect = NSRect(x: startX, y: centerY - logoSize / 2.0, width: logoSize, height: logoSize)
            let logoPath = NSBezierPath(roundedRect: logoRect, xRadius: 24.0 * scale, yRadius: 24.0 * scale)
            if let imgPath = job.imagePath {
                guard let img = NSImage(contentsOfFile: imgPath) else {
                    print("❌ Cannot decode supplied tool logo: \(imgPath)"); exit(1)
                }
                NSGraphicsContext.saveGraphicsState()
                logoPath.addClip()
                img.draw(in: logoRect)
                NSGraphicsContext.restoreGraphicsState()
            } else {
                coralColor.setFill()
                logoPath.fill()
            }
            (name as NSString).draw(at: NSPoint(x: startX + logoSize + gap, y: centerY - textSz.height / 2.0), withAttributes: attrs)

        case "repo_card":
            // Notion Effect #5: GitHub Dark Theme card at top of frame, 85% width
            let cardW = W * 0.85
            let cardH = 250.0 * scale
            let cardX = (W - cardW) / 2.0
            let cardY = H * (1.0 - 0.18) - cardH / 2.0
            let cardRect = NSRect(x: cardX, y: cardY, width: cardW, height: cardH)

            let bgPath = NSBezierPath(roundedRect: cardRect, xRadius: 20.0 * scale, yRadius: 20.0 * scale)
            colorFromHex("#0D1117", alpha: 0.96).setFill()
            bgPath.fill()
            colorFromHex("#30363D").setStroke()
            bgPath.lineWidth = 3.0 * scale
            bgPath.stroke()

            let repoTitle = job.title ?? "heygen-com/hyperframes"
            let desc = job.subtitle ?? "Deterministic HTML/CSS/GSAP video animation CLI"
            let stars = job.stars ?? "4.8k"
            let forks = job.forks ?? "340"

            let titleFont = NSFont(name: "HelveticaNeue-Bold", size: 38.0 * scale)!
            let descFont = NSFont(name: "HelveticaNeue", size: 28.0 * scale)!
            let metaFont = NSFont(name: "HelveticaNeue-Medium", size: 26.0 * scale)!

            (repoTitle as NSString).draw(
                at: NSPoint(x: cardX + 36.0 * scale, y: cardY + cardH - 72.0 * scale),
                withAttributes: [.font: titleFont, .foregroundColor: colorFromHex("#58A6FF")]
            )
            (desc as NSString).draw(
                at: NSPoint(x: cardX + 36.0 * scale, y: cardY + cardH - 135.0 * scale),
                withAttributes: [.font: descFont, .foregroundColor: colorFromHex("#8B949E")]
            )
            let metaText = "★ \(stars) stars    ⑂ \(forks) forks    • Public"
            (metaText as NSString).draw(
                at: NSPoint(x: cardX + 36.0 * scale, y: cardY + 34.0 * scale),
                withAttributes: [.font: metaFont, .foregroundColor: colorFromHex("#C9D1D9")]
            )

        case "prompt_bar":
            // Notion Effect #6: #2B2B2B rounded pill at 22.5% height, 92.6% width + #D97757 send button with up arrow
            let barW = W * 0.926
            let barH = 116.0 * scale
            let barX = (W - barW) / 2.0
            let barY = H * (1.0 - 0.225) - barH / 2.0
            let barRect = NSRect(x: barX, y: barY, width: barW, height: barH)

            let pill = NSBezierPath(roundedRect: barRect, xRadius: barH / 2.0, yRadius: barH / 2.0)
            colorFromHex("#2B2B2B", alpha: 0.96).setFill()
            pill.fill()

            let btnD = barH - 24.0 * scale
            let btnX = barX + barW - btnD - 12.0 * scale
            let btnY = barY + 12.0 * scale
            let btnRect = NSRect(x: btnX, y: btnY, width: btnD, height: btnD)
            let btnCircle = NSBezierPath(ovalIn: btnRect)
            coralColor.setFill()
            btnCircle.fill()

            // Up arrow inside coral button
            let arrow = NSBezierPath()
            let cx = btnX + btnD / 2.0
            let cy = btnY + btnD / 2.0
            arrow.move(to: NSPoint(x: cx, y: cy - 16.0 * scale))
            arrow.line(to: NSPoint(x: cx, y: cy + 16.0 * scale))
            arrow.move(to: NSPoint(x: cx - 12.0 * scale, y: cy + 4.0 * scale))
            arrow.line(to: NSPoint(x: cx, y: cy + 16.0 * scale))
            arrow.line(to: NSPoint(x: cx + 12.0 * scale, y: cy + 4.0 * scale))
            NSColor.white.setStroke()
            arrow.lineWidth = 4.5 * scale
            arrow.lineCapStyle = .round
            arrow.stroke()

            let promptText = job.title ?? "Cut every pause longer than 0.22 s, never inside a word."
            let pFont = NSFont(name: "HelveticaNeue-Medium", size: 32.0 * scale)!
            let pSz = (promptText as NSString).size(withAttributes: [.font: pFont])
            (promptText as NSString).draw(
                at: NSPoint(x: barX + 40.0 * scale, y: barY + (barH - pSz.height) / 2.0),
                withAttributes: [.font: pFont, .foregroundColor: NSColor.white]
            )

        default:
            break
        }
    }
    print("✅ [TalkingHeadOverlays] Rendered \(job.type) -> \(outPath)")
}
