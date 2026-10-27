import Cocoa
import CoreGraphics

let assetsDir = "/Users/arthurandersen/Documents/AI_Video_Editor_Gemini/VOX-TEST_race/02_assets"
try? FileManager.default.createDirectory(atPath: assetsDir, withIntermediateDirectories: true, attributes: nil)

// MARK: - Color Palette
let colorCream = NSColor(calibratedRed: 0.957, green: 0.929, blue: 0.871, alpha: 1.0)
let colorNavy = NSColor(calibratedRed: 0.180, green: 0.251, blue: 0.341, alpha: 1.0)
let colorCoral = NSColor(calibratedRed: 0.894, green: 0.341, blue: 0.180, alpha: 1.0)
let colorYellow = NSColor(calibratedRed: 1.000, green: 0.835, blue: 0.122, alpha: 1.0)
let colorInk = NSColor(calibratedRed: 0.098, green: 0.090, blue: 0.075, alpha: 1.0)
let colorWhite = NSColor.white

func createTransparentCanvas(w: Int, h: Int) -> (NSBitmapImageRep, NSGraphicsContext) {
    let rep = NSBitmapImageRep(
        bitmapDataPlanes: nil,
        pixelsWide: w,
        pixelsHigh: h,
        bitsPerSample: 8,
        samplesPerPixel: 4,
        hasAlpha: true,
        isPlanar: false,
        colorSpaceName: .deviceRGB,
        bytesPerRow: w * 4,
        bitsPerPixel: 32
    )!
    let ctx = NSGraphicsContext(bitmapImageRep: rep)!
    NSGraphicsContext.current = ctx
    
    // Clear transparent
    ctx.cgContext.clear(CGRect(x: 0, y: 0, width: w, height: h))
    return (rep, ctx)
}

func savePNG(_ rep: NSBitmapImageRep, _ filename: String) {
    let url = URL(fileURLWithPath: "\(assetsDir)/\(filename)")
    let data = rep.representation(using: .png, properties: [:])!
    try! data.write(to: url)
    print("Saved asset: \(filename) (\(data.count) bytes)")
}

func drawTornPaperCard(rect: NSRect, fillColor: NSColor) {
    let ctx = NSGraphicsContext.current!.cgContext
    ctx.saveGState()
    
    let sh = NSShadow()
    sh.shadowColor = NSColor(calibratedWhite: 0.0, alpha: 0.28)
    sh.shadowBlurRadius = 14.0
    sh.shadowOffset = NSSize(width: 0, height: -6)
    sh.set()
    
    let path = NSBezierPath()
    let step: CGFloat = 16.0
    path.move(to: NSPoint(x: rect.minX, y: rect.minY))
    var curX = rect.minX
    while curX < rect.maxX {
        curX += step
        let jitter = CGFloat(sin(Double(curX * 0.2)) * 3.0)
        path.line(to: NSPoint(x: min(curX, rect.maxX), y: rect.minY + jitter))
    }
    var curY = rect.minY
    while curY < rect.maxY {
        curY += step
        let jitter = CGFloat(cos(Double(curY * 0.16)) * 3.0)
        path.line(to: NSPoint(x: rect.maxX + jitter, y: min(curY, rect.maxY)))
    }
    while curX > rect.minX {
        curX -= step
        let jitter = CGFloat(sin(Double(curX * 0.22)) * 3.0)
        path.line(to: NSPoint(x: max(curX, rect.minX), y: rect.maxY + jitter))
    }
    while curY > rect.minY {
        curY -= step
        let jitter = CGFloat(cos(Double(curY * 0.18)) * 3.0)
        path.line(to: NSPoint(x: rect.minX + jitter, y: max(curY, rect.minY)))
    }
    path.close()
    
    colorWhite.setFill()
    path.fill()
    
    fillColor.setFill()
    NSBezierPath(rect: rect.insetBy(dx: 12, dy: 12)).fill()
    ctx.restoreGState()
}

// 1. Beat 1 Runners (5 runners)
for i in 1...5 {
    let (rep, _) = createTransparentCanvas(w: 300, h: 420)
    let cardRect = NSRect(x: 40, y: 40, width: 220, height: 340)
    let cColor = (i % 2 == 1) ? colorNavy : colorCoral
    drawTornPaperCard(rect: cardRect, fillColor: cColor)
    // Runner silhouette cut-out inside
    colorCream.setFill()
    let head = NSBezierPath(ovalIn: NSRect(x: 120, y: 260, width: 60, height: 60))
    let torso = NSBezierPath(roundedRect: NSRect(x: 105, y: 120, width: 90, height: 130), xRadius: 16, yRadius: 16)
    head.fill(); torso.fill()
    colorYellow.setFill()
    NSBezierPath(rect: NSRect(x: 115, y: 160, width: 70, height: 20)).fill() // bib
    savePNG(rep, "beat01_runner-\(i).png")
}

// Beat 1 Yellow start line
do {
    let (rep, _) = createTransparentCanvas(w: 800, h: 120)
    colorYellow.setFill()
    let sh = NSShadow()
    sh.shadowColor = NSColor(calibratedWhite: 0.0, alpha: 0.3)
    sh.shadowBlurRadius = 8; sh.shadowOffset = NSSize(width: 0, height: -4); sh.set()
    let p = NSBezierPath(roundedRect: NSRect(x: 30, y: 35, width: 740, height: 50), xRadius: 8, yRadius: 8)
    p.fill()
    savePNG(rep, "beat01_yellow-start-line.png")
}

// 2. Beat 2 Desk Row & Graduation Cap
do {
    let (rep, _) = createTransparentCanvas(w: 720, h: 220)
    for c in 0..<3 {
        let r = NSRect(x: 40 + c * 220, y: 40, width: 200, height: 140)
        drawTornPaperCard(rect: NSRect(x: CGFloat(r.origin.x), y: CGFloat(r.origin.y), width: CGFloat(r.size.width), height: CGFloat(r.size.height)), fillColor: colorNavy)
        colorCream.setFill()
        NSRect(x: r.minX + 20, y: r.minY + 50, width: r.width - 40, height: 22).fill()
    }
    savePNG(rep, "beat02_desk-row.png")
}

do {
    let (rep, ctx) = createTransparentCanvas(w: 360, h: 360)
    ctx.cgContext.saveGState()
    ctx.cgContext.translateBy(x: 180, y: 180)
    let sh = NSShadow(); sh.shadowColor = NSColor(calibratedWhite: 0.0, alpha: 0.35); sh.shadowBlurRadius = 14; sh.shadowOffset = NSSize(width: 0, height: -8); sh.set()
    let dia = NSBezierPath()
    dia.move(to: NSPoint(x: 0, y: 110)); dia.line(to: NSPoint(x: 140, y: 0)); dia.line(to: NSPoint(x: 0, y: -110)); dia.line(to: NSPoint(x: -140, y: 0)); dia.close()
    colorWhite.setFill(); dia.fill()
    let innerDia = NSBezierPath()
    innerDia.move(to: NSPoint(x: 0, y: 95)); innerDia.line(to: NSPoint(x: 125, y: 0)); innerDia.line(to: NSPoint(x: 0, y: -95)); innerDia.line(to: NSPoint(x: -125, y: 0)); innerDia.close()
    colorInk.setFill(); innerDia.fill()
    colorCoral.setStroke()
    let tassel = NSBezierPath(); tassel.lineWidth = 4; tassel.move(to: NSPoint(x: 0, y: 0)); tassel.curve(to: NSPoint(x: 80, y: -50), controlPoint1: NSPoint(x: 35, y: 10), controlPoint2: NSPoint(x: 65, y: -20)); tassel.stroke()
    colorYellow.setFill(); NSBezierPath(ovalIn: NSRect(x: -10, y: -10, width: 20, height: 20)).fill()
    ctx.cgContext.restoreGState()
    savePNG(rep, "beat02_grad-cap.png")
}

// 3. Beat 3 Cards (House, City, Handshake)
let cardDefs: [(String, String, NSColor)] = [
    ("beat03_card-house.png", "HOUSE", colorCoral),
    ("beat03_card-city.png", "CITY", colorNavy),
    ("beat03_card-handshake.png", "HANDSHAKE", colorYellow)
]
for (fname, type, accent) in cardDefs {
    let (rep, _) = createTransparentCanvas(w: 420, h: 580)
    let cardRect = NSRect(x: 30, y: 30, width: 360, height: 520)
    drawTornPaperCard(rect: cardRect, fillColor: colorCream)
    accent.setStroke()
    let inner = NSBezierPath(rect: cardRect.insetBy(dx: 24, dy: 24))
    inner.lineWidth = 4.0; inner.stroke()
    if type == "HOUSE" {
        colorCoral.setFill()
        let roof = NSBezierPath(); roof.move(to: NSPoint(x: 210, y: 400)); roof.line(to: NSPoint(x: 320, y: 290)); roof.line(to: NSPoint(x: 100, y: 290)); roof.close(); roof.fill()
        NSBezierPath(rect: NSRect(x: 125, y: 160, width: 170, height: 130)).fill()
    } else if type == "CITY" {
        colorNavy.setFill()
        NSBezierPath(rect: NSRect(x: 100, y: 160, width: 55, height: 160)).fill()
        NSBezierPath(rect: NSRect(x: 160, y: 160, width: 65, height: 210)).fill()
        NSBezierPath(rect: NSRect(x: 230, y: 160, width: 50, height: 140)).fill()
        NSBezierPath(rect: NSRect(x: 285, y: 160, width: 45, height: 180)).fill()
    } else if type == "HANDSHAKE" {
        colorInk.setFill()
        NSBezierPath(roundedRect: NSRect(x: 100, y: 250, width: 110, height: 60), xRadius: 10, yRadius: 10).fill()
        colorCoral.setFill()
        NSBezierPath(roundedRect: NSRect(x: 210, y: 250, width: 110, height: 60), xRadius: 10, yRadius: 10).fill()
        colorYellow.setFill()
        NSBezierPath(ovalIn: NSRect(x: 185, y: 255, width: 50, height: 50)).fill()
    }
    savePNG(rep, fname)
}

// 4. Beat 4 Smartphone & Notification Cards
do {
    let (rep, _) = createTransparentCanvas(w: 460, h: 900)
    let pRect = NSRect(x: 30, y: 30, width: 400, height: 840)
    drawTornPaperCard(rect: pRect, fillColor: colorInk)
    colorNavy.setFill()
    NSBezierPath(roundedRect: NSRect(x: 55, y: 90, width: 350, height: 720), xRadius: 24, yRadius: 24).fill()
    savePNG(rep, "beat04_phone-body.png")
}

let notifIcons: [(String, NSColor)] = [
    ("beat04_notif-ring.png", colorYellow),
    ("beat04_notif-key.png", colorCoral),
    ("beat04_notif-badge.png", colorNavy),
    ("beat04_notif-heart.png", colorCoral),
    ("beat04_notif-dollar.png", colorYellow),
    ("beat04_notif-trophy.png", colorYellow)
]
for (fname, accent) in notifIcons {
    let (rep, _) = createTransparentCanvas(w: 360, h: 160)
    let r = NSRect(x: 20, y: 20, width: 320, height: 120)
    drawTornPaperCard(rect: r, fillColor: colorCream)
    accent.setFill()
    NSBezierPath(ovalIn: NSRect(x: 45, y: 50, width: 60, height: 60)).fill()
    colorNavy.setFill()
    NSBezierPath(roundedRect: NSRect(x: 125, y: 85, width: 180, height: 16), xRadius: 4, yRadius: 4).fill()
    colorNavy.withAlphaComponent(0.4).setFill()
    NSBezierPath(roundedRect: NSRect(x: 125, y: 55, width: 120, height: 14), xRadius: 4, yRadius: 4).fill()
    savePNG(rep, fname)
}

// 5. Beat 5 Checkered Finish Flag & Runners
do {
    let (rep, _) = createTransparentCanvas(w: 240, h: 360)
    colorInk.setStroke()
    let pole = NSBezierPath(); pole.lineWidth = 6; pole.move(to: NSPoint(x: 200, y: 20)); pole.line(to: NSPoint(x: 200, y: 340)); pole.stroke()
    for r in 0..<4 {
        for c in 0..<5 {
            let col = (r + c) % 2 == 0 ? colorInk : colorWhite
            col.setFill()
            NSRect(x: 50 + c * 30, y: 180 + r * 30, width: 30, height: 30).fill()
        }
    }
    savePNG(rep, "beat05_top-track-flag.png")
}

// Beat 6 Milestone Stamps (Wedding, Shop, Diploma)
let stampDefs: [(String, String, NSColor)] = [
    ("beat06_stamp-wedding.png", "WEDDING", colorCoral),
    ("beat06_stamp-shop.png", "SHOP", colorNavy),
    ("beat06_stamp-diploma.png", "DIPLOMA", colorCoral)
]
for (fname, type, accent) in stampDefs {
    let (rep, _) = createTransparentCanvas(w: 260, h: 300)
    let sRect = NSRect(x: 20, y: 20, width: 220, height: 260)
    drawTornPaperCard(rect: sRect, fillColor: accent)
    if type == "WEDDING" {
        colorYellow.setStroke()
        let r1 = NSBezierPath(ovalIn: NSRect(x: 60, y: 120, width: 70, height: 70))
        let r2 = NSBezierPath(ovalIn: NSRect(x: 100, y: 100, width: 70, height: 70))
        r1.lineWidth = 8; r2.lineWidth = 8; r1.stroke(); r2.stroke()
    } else if type == "SHOP" {
        colorYellow.setFill()
        let rf = NSBezierPath(); rf.move(to: NSPoint(x: 130, y: 220)); rf.line(to: NSPoint(x: 200, y: 160)); rf.line(to: NSPoint(x: 60, y: 160)); rf.close(); rf.fill()
        colorCream.setFill(); NSBezierPath(rect: NSRect(x: 75, y: 70, width: 110, height: 90)).fill()
    } else if type == "DIPLOMA" {
        colorCream.setFill(); NSBezierPath(roundedRect: NSRect(x: 50, y: 110, width: 160, height: 70), xRadius: 14, yRadius: 14).fill()
        colorYellow.setFill(); NSBezierPath(rect: NSRect(x: 115, y: 95, width: 30, height: 100)).fill()
    }
    savePNG(rep, fname)
}

// Beat 7 Sprinter & Marathoner
do {
    let (rep, _) = createTransparentCanvas(w: 400, h: 620)
    let sRect = NSRect(x: 20, y: 20, width: 360, height: 580)
    drawTornPaperCard(rect: sRect, fillColor: colorCoral)
    colorCream.setFill()
    NSBezierPath(ovalIn: NSRect(x: 240, y: 380, width: 70, height: 70)).fill()
    NSBezierPath(roundedRect: NSRect(x: 120, y: 280, width: 160, height: 80), xRadius: 20, yRadius: 20).fill()
    colorInk.setFill()
    let blk = NSBezierPath(); blk.move(to: NSPoint(x: 60, y: 80)); blk.line(to: NSPoint(x: 140, y: 160)); blk.line(to: NSPoint(x: 140, y: 80)); blk.close(); blk.fill()
    savePNG(rep, "beat07_sprinter-blocks.png")
}
do {
    let (rep, _) = createTransparentCanvas(w: 400, h: 700)
    let mRect = NSRect(x: 20, y: 20, width: 360, height: 660)
    drawTornPaperCard(rect: mRect, fillColor: colorNavy)
    colorCream.setFill()
    NSBezierPath(ovalIn: NSRect(x: 155, y: 460, width: 75, height: 75)).fill()
    NSBezierPath(roundedRect: NSRect(x: 140, y: 200, width: 100, height: 260), xRadius: 22, yRadius: 22).fill()
    colorYellow.setFill(); NSBezierPath(rect: NSRect(x: 150, y: 300, width: 80, height: 70)).fill()
    savePNG(rep, "beat07_marathoner.png")
}

// Beat 8 Two Columns & Yellow Oval
do {
    let (rep, _) = createTransparentCanvas(w: 420, h: 1100)
    let cRect = NSRect(x: 20, y: 20, width: 380, height: 1060)
    drawTornPaperCard(rect: cRect, fillColor: colorNavy.withAlphaComponent(0.25))
    colorNavy.withAlphaComponent(0.40).setFill()
    NSBezierPath(ovalIn: NSRect(x: 165, y: 720, width: 90, height: 90)).fill()
    NSBezierPath(roundedRect: NSRect(x: 150, y: 400, width: 120, height: 300), xRadius: 24, yRadius: 24).fill()
    savePNG(rep, "beat08_col-faded.png")
}
do {
    let (rep, _) = createTransparentCanvas(w: 420, h: 1100)
    let cRect = NSRect(x: 20, y: 20, width: 380, height: 1060)
    drawTornPaperCard(rect: cRect, fillColor: colorCoral)
    colorYellow.setFill(); NSBezierPath(ovalIn: NSRect(x: 165, y: 720, width: 90, height: 90)).fill()
    colorCream.setFill(); NSBezierPath(roundedRect: NSRect(x: 150, y: 400, width: 120, height: 300), xRadius: 24, yRadius: 24).fill()
    savePNG(rep, "beat08_col-now.png")
}
do {
    let (rep, ctx) = createTransparentCanvas(w: 920, h: 1200)
    ctx.cgContext.saveGState()
    colorYellow.setStroke()
    let oval = NSBezierPath(ovalIn: NSRect(x: 20, y: 20, width: 880, height: 1160))
    oval.lineWidth = 16; oval.stroke()
    ctx.cgContext.restoreGState()
    savePNG(rep, "beat08_yellow-oval.png")
}

// Beat 9 Lone Runner
do {
    let (rep, _) = createTransparentCanvas(w: 240, h: 360)
    let rRect = NSRect(x: 30, y: 30, width: 180, height: 300)
    drawTornPaperCard(rect: rRect, fillColor: colorNavy)
    colorCoral.setFill(); NSBezierPath(roundedRect: NSRect(x: 80, y: 140, width: 80, height: 110), xRadius: 14, yRadius: 14).fill()
    colorCream.setFill(); NSBezierPath(ovalIn: NSRect(x: 90, y: 250, width: 60, height: 60)).fill()
    savePNG(rep, "beat09_lone-runner.png")
}

// Textures (Paper, Halftone, Tape)
do {
    let (rep, ctx) = createTransparentCanvas(w: 1080, h: 1920)
    colorCream.setFill(); NSRect(x: 0, y: 0, width: 1080, height: 1920).fill()
    for i in 0..<180 {
        let y = CGFloat((i * 47) % 1920); let x = CGFloat((i * 83) % 1080); let w = CGFloat(60 + (i * 13) % 240)
        NSColor(calibratedWhite: 0.0, alpha: CGFloat(0.015 + Double(i % 5) * 0.008)).setStroke()
        let path = NSBezierPath(); path.lineWidth = CGFloat(1 + (i % 3)); path.move(to: NSPoint(x: x, y: y)); path.line(to: NSPoint(x: x + w, y: y + CGFloat((i % 7) - 3))); path.stroke()
    }
    savePNG(rep, "paper_cream_texture.png")
}
do {
    let (rep, _) = createTransparentCanvas(w: 600, h: 600)
    colorNavy.withAlphaComponent(0.25).setFill()
    var y: CGFloat = 10
    while y <= 590 {
        var x: CGFloat = 10
        while x <= 590 {
            NSBezierPath(ovalIn: NSRect(x: x - 3, y: y - 3, width: 6, height: 6)).fill()
            x += 20
        }
        y += 20
    }
    savePNG(rep, "halftone_dot_texture.png")
}
do {
    let (rep, ctx) = createTransparentCanvas(w: 240, h: 80)
    let tapeRect = NSRect(x: 20, y: 15, width: 200, height: 50)
    let tapeColor = NSColor(calibratedRed: 0.96, green: 0.93, blue: 0.85, alpha: 0.82)
    tapeColor.setFill(); tapeRect.fill()
    savePNG(rep, "tape_strip.png")
}

// MARK: - Generate Checkerboard Contact Sheet
print("Generating checkerboard contact sheet for all assets...")
let contactW = 1920
let contactH = 1080
let repContact = NSBitmapImageRep(
    bitmapDataPlanes: nil,
    pixelsWide: contactW,
    pixelsHigh: contactH,
    bitsPerSample: 8,
    samplesPerPixel: 4,
    hasAlpha: true,
    isPlanar: false,
    colorSpaceName: .deviceRGB,
    bytesPerRow: contactW * 4,
    bitsPerPixel: 32
)!
let ctxContact = NSGraphicsContext(bitmapImageRep: repContact)!
NSGraphicsContext.current = ctxContact

// Draw standard transparency checkerboard
let sqSize: CGFloat = 32.0
var cY: CGFloat = 0
while cY < CGFloat(contactH) {
    var cX: CGFloat = 0
    while cX < CGFloat(contactW) {
        let isLight = (Int(cX / sqSize) + Int(cY / sqSize)) % 2 == 0
        let c = isLight ? NSColor(calibratedWhite: 0.82, alpha: 1.0) : NSColor(calibratedWhite: 0.68, alpha: 1.0)
        c.setFill()
        NSRect(x: cX, y: cY, width: sqSize, height: sqSize).fill()
        cX += sqSize
    }
    cY += sqSize
}

// Place thumbnails of 18 key cutouts in a 6x3 grid
let fileList = [
    "beat01_runner-1.png", "beat01_runner-3.png", "beat01_yellow-start-line.png",
    "beat02_desk-row.png", "beat02_grad-cap.png", "beat03_card-house.png",
    "beat03_card-city.png", "beat03_card-handshake.png", "beat04_phone-body.png",
    "beat04_notif-ring.png", "beat04_notif-key.png", "beat05_top-track-flag.png",
    "beat06_stamp-wedding.png", "beat06_stamp-shop.png", "beat06_stamp-diploma.png",
    "beat07_sprinter-blocks.png", "beat07_marathoner.png", "beat08_yellow-oval.png"
]

let tCols = 6
let tRows = 3
let tCellW = CGFloat(contactW / tCols)
let tCellH = CGFloat(contactH / tRows)

for (idx, fn) in fileList.enumerated() {
    let col = idx % tCols
    let row = idx / tCols
    let x = CGFloat(col) * tCellW
    let y = CGFloat(tRows - 1 - row) * tCellH
    let cellRect = NSRect(x: x + 15, y: y + 15, width: tCellW - 30, height: tCellH - 30)
    
    let path = "\(assetsDir)/\(fn)"
    if let img = NSImage(contentsOfFile: path) {
        img.draw(in: cellRect)
    }
    
    // Label
    let pCenter = NSMutableParagraphStyle(); pCenter.alignment = .center
    let font = NSFont(name: "Arial-Bold", size: 14) ?? NSFont.boldSystemFont(ofSize: 14)
    let attrs: [NSAttributedString.Key: Any] = [
        .font: font,
        .foregroundColor: NSColor(calibratedWhite: 0.1, alpha: 0.9),
        .paragraphStyle: pCenter
    ]
    NSAttributedString(string: fn.replacingOccurrences(of: ".png", with: ""), attributes: attrs).draw(in: NSRect(x: x, y: y + 5, width: tCellW, height: 20))
}

let contactOut = "\(assetsDir)/checkerboard-contact.jpg"
let cData = repContact.representation(using: .jpeg, properties: [.compressionFactor: 0.90])!
try! cData.write(to: URL(fileURLWithPath: contactOut))
print("Saved checkerboard contact sheet to \(contactOut)")
