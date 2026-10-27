import Cocoa
import CoreGraphics

let width = 1080
let height = 1920
let postersDir = "/Users/arthurandersen/Documents/AI_Video_Editor_Gemini/VOX-TEST_race/01_storyboard/posters"

try? FileManager.default.createDirectory(atPath: postersDir, withIntermediateDirectories: true, attributes: nil)

// MARK: - Color Palette (Theme A: Classic Vox)
let colorCream = NSColor(calibratedRed: 0.957, green: 0.929, blue: 0.871, alpha: 1.0) // #F4EDDE
let colorCreamDark = NSColor(calibratedRed: 0.910, green: 0.875, blue: 0.805, alpha: 1.0)
let colorNavy = NSColor(calibratedRed: 0.180, green: 0.251, blue: 0.341, alpha: 1.0)  // #2E4057
let colorNavyDark = NSColor(calibratedRed: 0.110, green: 0.155, blue: 0.215, alpha: 1.0)
let colorCoral = NSColor(calibratedRed: 0.894, green: 0.341, blue: 0.180, alpha: 1.0) // #E4572E
let colorYellow = NSColor(calibratedRed: 1.000, green: 0.835, blue: 0.122, alpha: 1.0) // #FFD51F (Vox Yellow)
let colorInk = NSColor(calibratedRed: 0.098, green: 0.090, blue: 0.075, alpha: 1.0)    // #191713
let colorWhite = NSColor.white
let colorHalftone = NSColor(calibratedRed: 0.45, green: 0.48, blue: 0.52, alpha: 0.35)

// MARK: - Drawing Helpers

func createCanvas() -> (NSBitmapImageRep, NSGraphicsContext) {
    let rep = NSBitmapImageRep(
        bitmapDataPlanes: nil,
        pixelsWide: width,
        pixelsHigh: height,
        bitsPerSample: 8,
        samplesPerPixel: 4,
        hasAlpha: true,
        isPlanar: false,
        colorSpaceName: .deviceRGB,
        bytesPerRow: width * 4,
        bitsPerPixel: 32
    )!
    let ctx = NSGraphicsContext(bitmapImageRep: rep)!
    NSGraphicsContext.current = ctx
    return (rep, ctx)
}

func saveJPEG(_ rep: NSBitmapImageRep, _ filename: String) {
    let url = URL(fileURLWithPath: "\(postersDir)/\(filename)")
    let data = rep.representation(using: .jpeg, properties: [.compressionFactor: 0.92])!
    try! data.write(to: url)
    print("Saved poster: \(filename) (\(data.count) bytes)")
}

func drawPaperBackground(ctx: CGContext) {
    // 1. Base cream paper
    colorCream.setFill()
    NSRect(x: 0, y: 0, width: width, height: height).fill()
    
    // 2. Subtle organic paper fiber streaks
    ctx.saveGState()
    for i in 0..<180 {
        let y = CGFloat((i * 47) % height)
        let x = CGFloat((i * 83) % width)
        let w = CGFloat(60 + (i * 13) % 240)
        let alpha = CGFloat(0.015 + Double(i % 5) * 0.008)
        NSColor(calibratedWhite: 0.0, alpha: alpha).setStroke()
        let path = NSBezierPath()
        path.lineWidth = CGFloat(1 + (i % 3))
        path.move(to: NSPoint(x: x, y: y))
        path.line(to: NSPoint(x: x + w, y: y + CGFloat((i % 7) - 3)))
        path.stroke()
    }
    ctx.restoreGState()
}

func drawHalftoneGrid(rect: NSRect, dotColor: NSColor, dotSpacing: CGFloat, dotRadius: CGFloat) {
    dotColor.setFill()
    var y = rect.minY
    while y <= rect.maxY {
        var x = rect.minX
        while x <= rect.maxX {
            let p = NSBezierPath(ovalIn: NSRect(x: x - dotRadius, y: y - dotRadius, width: dotRadius * 2, height: dotRadius * 2))
            p.fill()
            x += dotSpacing
        }
        y += dotSpacing
    }
}

func drawTape(at point: NSPoint, width w: CGFloat, height h: CGFloat, angleDeg: CGFloat) {
    let ctx = NSGraphicsContext.current!.cgContext
    ctx.saveGState()
    ctx.translateBy(x: point.x, y: point.y)
    ctx.rotate(by: angleDeg * .pi / 180.0)
    
    // Soft shadow under tape
    let sh = NSShadow()
    sh.shadowColor = NSColor(calibratedWhite: 0.0, alpha: 0.20)
    sh.shadowBlurRadius = 6.0
    sh.shadowOffset = NSSize(width: 0, height: -3)
    sh.set()
    
    // Translucent masking tape body
    let tapeRect = NSRect(x: -w/2, y: -h/2, width: w, height: h)
    let tapeColor = NSColor(calibratedRed: 0.96, green: 0.93, blue: 0.85, alpha: 0.78)
    tapeColor.setFill()
    tapeRect.fill()
    
    // Jagged cut ends on left and right
    ctx.restoreGState()
}

func drawTornPaperCard(rect: NSRect, fillColor: NSColor, addShadow: Bool = true) {
    let ctx = NSGraphicsContext.current!.cgContext
    ctx.saveGState()
    
    if addShadow {
        let sh = NSShadow()
        sh.shadowColor = NSColor(calibratedWhite: 0.0, alpha: 0.25)
        sh.shadowBlurRadius = 14.0
        sh.shadowOffset = NSSize(width: 0, height: -8)
        sh.set()
    }
    
    // Outer white torn border path
    let path = NSBezierPath()
    let step: CGFloat = 20.0
    
    // Bottom edge
    path.move(to: NSPoint(x: rect.minX, y: rect.minY))
    var curX = rect.minX
    while curX < rect.maxX {
        curX += step
        let jitter = CGFloat(sin(Double(curX * 0.15)) * 3.5)
        path.line(to: NSPoint(x: min(curX, rect.maxX), y: rect.minY + jitter))
    }
    // Right edge
    var curY = rect.minY
    while curY < rect.maxY {
        curY += step
        let jitter = CGFloat(cos(Double(curY * 0.12)) * 3.5)
        path.line(to: NSPoint(x: rect.maxX + jitter, y: min(curY, rect.maxY)))
    }
    // Top edge
    while curX > rect.minX {
        curX -= step
        let jitter = CGFloat(sin(Double(curX * 0.18)) * 3.5)
        path.line(to: NSPoint(x: max(curX, rect.minX), y: rect.maxY + jitter))
    }
    // Left edge
    while curY > rect.minY {
        curY -= step
        let jitter = CGFloat(cos(Double(curY * 0.14)) * 3.5)
        path.line(to: NSPoint(x: rect.minX + jitter, y: max(curY, rect.minY)))
    }
    path.close()
    
    // Fill white border
    colorWhite.setFill()
    path.fill()
    
    // Fill inner color with margin
    let innerRect = rect.insetBy(dx: 14, dy: 14)
    fillColor.setFill()
    let innerPath = NSBezierPath(rect: innerRect)
    innerPath.fill()
    
    ctx.restoreGState()
}

// MARK: - Beat 2: False Fairness (Desks & Graduation Caps)
func renderBeat02() {
    let (rep, ctx) = createCanvas()
    drawPaperBackground(ctx: ctx.cgContext)
    
    // Halftone textures in corners
    drawHalftoneGrid(rect: NSRect(x: 40, y: 1680, width: 320, height: 200), dotColor: colorNavy.withAlphaComponent(0.20), dotSpacing: 16, dotRadius: 3.5)
    drawHalftoneGrid(rect: NSRect(x: 740, y: 80, width: 300, height: 240), dotColor: colorCoral.withAlphaComponent(0.20), dotSpacing: 16, dotRadius: 3.5)
    
    // Decorative navy/coral geometric paper clippings
    let patch1 = NSBezierPath()
    patch1.move(to: NSPoint(x: 60, y: 1840))
    patch1.line(to: NSPoint(x: 340, y: 1840))
    patch1.line(to: NSPoint(x: 280, y: 1660))
    patch1.line(to: NSPoint(x: 60, y: 1700))
    patch1.close()
    colorNavy.setFill()
    patch1.fill()
    
    let patch2 = NSBezierPath()
    patch2.move(to: NSPoint(x: 820, y: 180))
    patch2.line(to: NSPoint(x: 1040, y: 100))
    patch2.line(to: NSPoint(x: 1040, y: 400))
    patch2.line(to: NSPoint(x: 760, y: 350))
    patch2.close()
    colorCoral.setFill()
    patch2.fill()
    
    // Draw 3 rows of identical wooden classroom desks receding in perspective
    let deskCols = 3
    let deskRows = 4
    for r in (0..<deskRows).reversed() {
        let t = CGFloat(r) / CGFloat(deskRows)
        let deskY = 320 + t * 580
        let scale = 1.0 - t * 0.38
        let w = 240 * scale
        let h = 120 * scale
        
        for c in 0..<deskCols {
            let deskX = 140 + CGFloat(c) * (280 * scale) + t * 40
            let dRect = NSRect(x: deskX, y: deskY, width: w, height: h)
            drawTornPaperCard(rect: dRect, fillColor: colorNavy.withAlphaComponent(0.85))
            
            // Desk surface wood strip
            colorCream.setFill()
            NSRect(x: dRect.minX + 20 * scale, y: dRect.minY + 40 * scale, width: dRect.width - 40 * scale, height: 18 * scale).fill()
        }
    }
    
    // Floating black graduation mortarboard caps tossed in the air with tassels
    let capPositions: [(CGFloat, CGFloat, CGFloat)] = [
        (260, 1260, 18),
        (540, 1420, -12),
        (820, 1300, 24),
        (380, 1080, -8),
        (700, 1120, 15)
    ]
    
    for (cx, cy, rot) in capPositions {
        ctx.cgContext.saveGState()
        ctx.cgContext.translateBy(x: cx, y: cy)
        ctx.cgContext.rotate(by: rot * .pi / 180.0)
        
        // Cap shadow
        let sh = NSShadow()
        sh.shadowColor = NSColor(calibratedWhite: 0.0, alpha: 0.32)
        sh.shadowBlurRadius = 18.0
        sh.shadowOffset = NSSize(width: 0, height: -10)
        sh.set()
        
        // White torn border diamond
        let diamond = NSBezierPath()
        diamond.move(to: NSPoint(x: 0, y: 70))
        diamond.line(to: NSPoint(x: 130, y: 0))
        diamond.line(to: NSPoint(x: 0, y: -70))
        diamond.line(to: NSPoint(x: -130, y: 0))
        diamond.close()
        colorWhite.setFill()
        diamond.fill()
        
        // Dark ink mortarboard cap body
        let innerDia = NSBezierPath()
        innerDia.move(to: NSPoint(x: 0, y: 58))
        innerDia.line(to: NSPoint(x: 114, y: 0))
        innerDia.line(to: NSPoint(x: 0, y: -58))
        innerDia.line(to: NSPoint(x: -114, y: 0))
        innerDia.close()
        colorInk.setFill()
        innerDia.fill()
        
        // Coral tassel cord
        colorCoral.setStroke()
        let tassel = NSBezierPath()
        tassel.lineWidth = 4.0
        tassel.move(to: NSPoint(x: 0, y: 0))
        tassel.curve(to: NSPoint(x: 75, y: -45), controlPoint1: NSPoint(x: 35, y: 10), controlPoint2: NSPoint(x: 60, y: -20))
        tassel.stroke()
        
        // Yellow button center
        colorYellow.setFill()
        NSBezierPath(ovalIn: NSRect(x: -8, y: -8, width: 16, height: 16)).fill()
        
        ctx.cgContext.restoreGState()
    }
    
    // Tape on corners
    drawTape(at: NSPoint(x: 120, y: 1840), width: 140, height: 46, angleDeg: 35)
    drawTape(at: NSPoint(x: 960, y: 1820), width: 140, height: 46, angleDeg: -40)
    drawTape(at: NSPoint(x: 140, y: 120), width: 130, height: 44, angleDeg: -30)
    drawTape(at: NSPoint(x: 940, y: 140), width: 130, height: 44, angleDeg: 35)
    
    saveJPEG(rep, "beat02_poster.jpg")
}

// MARK: - Beat 3: The Cards (House, Skyline, Handshake)
func renderBeat03() {
    let (rep, ctx) = createCanvas()
    drawPaperBackground(ctx: ctx.cgContext)
    
    // Halftone grid center
    drawHalftoneGrid(rect: NSRect(x: 100, y: 200, width: 880, height: 1520), dotColor: colorHalftone, dotSpacing: 22, dotRadius: 3.0)
    
    // Table surface wood grain lines
    ctx.cgContext.saveGState()
    for y in stride(from: 100, to: 1800, by: 120) {
        NSColor(calibratedRed: 0.88, green: 0.84, blue: 0.77, alpha: 0.6).setStroke()
        let line = NSBezierPath()
        line.lineWidth = 2.0
        line.move(to: NSPoint(x: 40, y: CGFloat(y)))
        line.line(to: NSPoint(x: 1040, y: CGFloat(y)))
        line.stroke()
    }
    ctx.cgContext.restoreGState()
    
    // 3 Oversized Playing Cards dealing onto table
    let cards: [(CGFloat, CGFloat, CGFloat, String, NSColor)] = [
        (540, 1340, -6, "HOUSE", colorCoral),
        (340, 780, 10, "CITY", colorNavy),
        (740, 750, -8, "HANDSHAKE", colorYellow)
    ]
    
    for (cx, cy, rot, type, accent) in cards {
        ctx.cgContext.saveGState()
        ctx.cgContext.translateBy(x: cx, y: cy)
        ctx.cgContext.rotate(by: rot * .pi / 180.0)
        
        let cardRect = NSRect(x: -180, y: -260, width: 360, height: 520)
        drawTornPaperCard(rect: cardRect, fillColor: colorCreamDark)
        
        // Card inner frame border
        accent.setStroke()
        let innerFrame = NSBezierPath(rect: cardRect.insetBy(dx: 24, dy: 24))
        innerFrame.lineWidth = 4.0
        innerFrame.stroke()
        
        // Card Icon Cutout
        if type == "HOUSE" {
            // Cutout house silhouette
            colorCoral.setFill()
            let roof = NSBezierPath()
            roof.move(to: NSPoint(x: 0, y: 130))
            roof.line(to: NSPoint(x: 110, y: 20))
            roof.line(to: NSPoint(x: -110, y: 20))
            roof.close()
            roof.fill()
            
            let base = NSBezierPath(rect: NSRect(x: -85, y: -110, width: 170, height: 130))
            base.fill()
            
            // Door
            colorCreamDark.setFill()
            NSBezierPath(rect: NSRect(x: -25, y: -110, width: 50, height: 75)).fill()
            // Chimney
            colorCoral.setFill()
            NSBezierPath(rect: NSRect(x: 45, y: 70, width: 30, height: 50)).fill()
        } else if type == "CITY" {
            // City Skyline silhouette
            colorNavy.setFill()
            let b1 = NSBezierPath(rect: NSRect(x: -110, y: -100, width: 55, height: 160))
            let b2 = NSBezierPath(rect: NSRect(x: -50, y: -100, width: 65, height: 210))
            let b3 = NSBezierPath(rect: NSRect(x: 20, y: -100, width: 50, height: 140))
            let b4 = NSBezierPath(rect: NSRect(x: 75, y: -100, width: 45, height: 180))
            b1.fill(); b2.fill(); b3.fill(); b4.fill()
            
            // Antenna spire
            colorYellow.setFill()
            NSBezierPath(rect: NSRect(x: -22, y: 110, width: 8, height: 50)).fill()
        } else if type == "HANDSHAKE" {
            // Handshake icon geometry
            colorInk.setFill()
            let h1 = NSBezierPath()
            h1.move(to: NSPoint(x: -120, y: 30))
            h1.line(to: NSPoint(x: -30, y: 50))
            h1.line(to: NSPoint(x: 10, y: -30))
            h1.line(to: NSPoint(x: -60, y: -50))
            h1.close()
            h1.fill()
            
            colorCoral.setFill()
            let h2 = NSBezierPath()
            h2.move(to: NSPoint(x: 120, y: 30))
            h2.line(to: NSPoint(x: 30, y: 50))
            h2.line(to: NSPoint(x: -10, y: -30))
            h2.line(to: NSPoint(x: 60, y: -50))
            h2.close()
            h2.fill()
            
            // Clasping fingers
            colorYellow.setFill()
            NSBezierPath(ovalIn: NSRect(x: -25, y: -20, width: 50, height: 40)).fill()
        }
        
        ctx.cgContext.restoreGState()
    }
    
    // Tape on card corners
    drawTape(at: NSPoint(x: 480, y: 1620), width: 120, height: 42, angleDeg: 12)
    drawTape(at: NSPoint(x: 160, y: 1800), width: 140, height: 46, angleDeg: -35)
    drawTape(at: NSPoint(x: 920, y: 1800), width: 140, height: 46, angleDeg: 35)
    
    saveJPEG(rep, "beat03_poster.jpg")
}

// MARK: - Beat 4: The Scoreboard (Smartphone & Overwhelming Notifications)
func renderBeat04() {
    let (rep, ctx) = createCanvas()
    drawPaperBackground(ctx: ctx.cgContext)
    
    // Large deep navy paper patch mounted in center
    let navyBackdrop = NSRect(x: 90, y: 240, width: 900, height: 1440)
    drawTornPaperCard(rect: navyBackdrop, fillColor: colorNavy)
    
    // Halftone dots inside navy sheet
    drawHalftoneGrid(rect: navyBackdrop.insetBy(dx: 40, dy: 40), dotColor: colorCream.withAlphaComponent(0.12), dotSpacing: 20, dotRadius: 2.8)
    
    // Hand-cut Smartphone cut-out in center
    ctx.cgContext.saveGState()
    let phoneRect = NSRect(x: 340, y: 540, width: 400, height: 840)
    drawTornPaperCard(rect: phoneRect, fillColor: colorInk)
    
    // Phone screen
    colorNavyDark.setFill()
    let screenRect = NSRect(x: 365, y: 600, width: 350, height: 720)
    NSBezierPath(roundedRect: screenRect, xRadius: 24, yRadius: 24).fill()
    
    // Speaker notch
    colorCream.setFill()
    NSBezierPath(roundedRect: NSRect(x: 490, y: 1290, width: 100, height: 12), xRadius: 6, yRadius: 6).fill()
    ctx.cgContext.restoreGState()
    
    // Floating Paper Notification Cards popping around the phone
    let notifs: [(CGFloat, CGFloat, CGFloat, String, NSColor)] = [
        (260, 1380, -10, "RING", colorYellow),
        (820, 1320, 12, "HOUSE_KEY", colorCoral),
        (240, 960, 6, "BADGE", colorCream),
        (840, 920, -8, "HEART", colorCoral),
        (260, 560, -14, "DOLLAR", colorYellow),
        (820, 520, 15, "TROPHY", colorYellow)
    ]
    
    for (nx, ny, rot, icon, accent) in notifs {
        ctx.cgContext.saveGState()
        ctx.cgContext.translateBy(x: nx, y: ny)
        ctx.cgContext.rotate(by: rot * .pi / 180.0)
        
        let nRect = NSRect(x: -160, y: -65, width: 320, height: 130)
        drawTornPaperCard(rect: nRect, fillColor: colorCream)
        
        // Icon badge circle on left
        accent.setFill()
        NSBezierPath(ovalIn: NSRect(x: -130, y: -35, width: 70, height: 70)).fill()
        
        // Notification fake text bars (pure graphic rectangles, no letters)
        colorNavy.setFill()
        NSBezierPath(roundedRect: NSRect(x: -45, y: 5, width: 170, height: 16), xRadius: 4, yRadius: 4).fill()
        colorHalftone.setFill()
        NSBezierPath(roundedRect: NSRect(x: -45, y: -25, width: 120, height: 14), xRadius: 4, yRadius: 4).fill()
        
        ctx.cgContext.restoreGState()
    }
    
    // Tape pieces
    drawTape(at: NSPoint(x: 200, y: 1700), width: 140, height: 44, angleDeg: -28)
    drawTape(at: NSPoint(x: 880, y: 1700), width: 140, height: 44, angleDeg: 30)
    drawTape(at: NSPoint(x: 540, y: 220), width: 160, height: 44, angleDeg: 4)
    
    saveJPEG(rep, "beat04_poster.jpg")
}

// MARK: - Beat 5: Lap 3 vs Lap 9 (Split Screen Strips)
func renderBeat05() {
    let (rep, ctx) = createCanvas()
    drawPaperBackground(ctx: ctx.cgContext)
    
    // Top Strip: Lap 9 (Finish line flag, runner ahead)
    let topStrip = NSRect(x: 60, y: 1020, width: 960, height: 820)
    drawTornPaperCard(rect: topStrip, fillColor: colorCreamDark)
    
    // Halftone top right
    drawHalftoneGrid(rect: NSRect(x: 680, y: 1380, width: 320, height: 420), dotColor: colorCoral.withAlphaComponent(0.22), dotSpacing: 18, dotRadius: 3.5)
    
    // Perspective track lanes top
    ctx.cgContext.saveGState()
    colorNavy.setStroke()
    for i in 0...4 {
        let path = NSBezierPath()
        path.lineWidth = 3.5
        path.move(to: NSPoint(x: 100 + CGFloat(i) * 180, y: 1060))
        path.line(to: NSPoint(x: 350 + CGFloat(i) * 90, y: 1780))
        path.stroke()
    }
    
    // Checkered Finish Flag
    let flagX: CGFloat = 820
    let flagY: CGFloat = 1360
    colorInk.setStroke()
    let pole = NSBezierPath()
    pole.lineWidth = 6.0
    pole.move(to: NSPoint(x: flagX, y: flagY - 140))
    pole.line(to: NSPoint(x: flagX, y: flagY + 180))
    pole.stroke()
    
    // Flag cloth
    for r in 0..<4 {
        for c in 0..<5 {
            let bColor = (r + c) % 2 == 0 ? colorInk : colorWhite
            bColor.setFill()
            NSRect(x: flagX - 150 + CGFloat(c) * 30, y: flagY + 40 + CGFloat(r) * 30, width: 30, height: 30).fill()
        }
    }
    
    // Runner 1 silhouette (near flag)
    colorCoral.setFill()
    let runner1 = NSBezierPath()
    runner1.appendOval(in: NSRect(x: 580, y: 1480, width: 50, height: 50)) // Head
    runner1.append(NSBezierPath(rect: NSRect(x: 575, y: 1340, width: 60, height: 140))) // Torso
    runner1.fill()
    ctx.cgContext.restoreGState()
    
    // Dashed divider line between strips
    ctx.cgContext.saveGState()
    colorInk.setStroke()
    let divider = NSBezierPath()
    divider.lineWidth = 6.0
    let dashes: [CGFloat] = [28.0, 18.0]
    divider.setLineDash(dashes, count: 2, phase: 0)
    divider.move(to: NSPoint(x: 40, y: 960))
    divider.line(to: NSPoint(x: 1040, y: 960))
    divider.stroke()
    ctx.cgContext.restoreGState()
    
    // Bottom Strip: Lap 3 (Runner far back, vast empty track)
    let bottomStrip = NSRect(x: 60, y: 80, width: 960, height: 820)
    drawTornPaperCard(rect: bottomStrip, fillColor: colorCream)
    
    // Halftone bottom left
    drawHalftoneGrid(rect: NSRect(x: 80, y: 120, width: 340, height: 360), dotColor: colorNavy.withAlphaComponent(0.20), dotSpacing: 18, dotRadius: 3.5)
    
    // Wide empty running track perspective lines
    ctx.cgContext.saveGState()
    colorCoral.setStroke()
    for i in 0...4 {
        let path = NSBezierPath()
        path.lineWidth = 3.5
        path.move(to: NSPoint(x: 80 + CGFloat(i) * 200, y: 120))
        path.line(to: NSPoint(x: 300 + CGFloat(i) * 110, y: 840))
        path.stroke()
    }
    
    // Distant runner 2 silhouette (small, far behind)
    colorNavy.setFill()
    let runner2 = NSBezierPath()
    runner2.appendOval(in: NSRect(x: 520, y: 620, width: 28, height: 28)) // Distant small head
    runner2.append(NSBezierPath(rect: NSRect(x: 516, y: 540, width: 36, height: 80))) // Distant torso
    runner2.fill()
    ctx.cgContext.restoreGState()
    
    // Tape pieces
    drawTape(at: NSPoint(x: 100, y: 1840), width: 140, height: 44, angleDeg: 35)
    drawTape(at: NSPoint(x: 960, y: 1840), width: 140, height: 44, angleDeg: -35)
    drawTape(at: NSPoint(x: 960, y: 100), width: 140, height: 44, angleDeg: 30)
    
    saveJPEG(rep, "beat05_poster.jpg")
}

// MARK: - Beat 6: The Real Timeline (Paper Timeline Strip & Milestones)
func renderBeat06() {
    let (rep, ctx) = createCanvas()
    drawPaperBackground(ctx: ctx.cgContext)
    
    // Halftone backgrounds
    drawHalftoneGrid(rect: NSRect(x: 60, y: 1400, width: 960, height: 400), dotColor: colorHalftone, dotSpacing: 20, dotRadius: 3.0)
    drawHalftoneGrid(rect: NSRect(x: 60, y: 120, width: 960, height: 400), dotColor: colorHalftone, dotSpacing: 20, dotRadius: 3.0)
    
    // Central horizontal paper timeline strip across cream
    let timelineRect = NSRect(x: 60, y: 880, width: 960, height: 160)
    drawTornPaperCard(rect: timelineRect, fillColor: colorNavy)
    
    // Yellow timeline guide line
    colorYellow.setFill()
    NSRect(x: 100, y: 952, width: 880, height: 16).fill()
    
    // Tick marks along the timeline
    colorWhite.setFill()
    for x in stride(from: 140, through: 940, by: 80) {
        NSRect(x: CGFloat(x) - 3, y: 935, width: 6, height: 50).fill()
    }
    
    // 3 Scattered Paper Stamp Badges
    // 1. Wedding at 24 (Left/Center bottom)
    let stamp1Rect = NSRect(x: 200, y: 520, width: 220, height: 260)
    drawTornPaperCard(rect: stamp1Rect, fillColor: colorCoral)
    // Two interlocking rings
    ctx.cgContext.saveGState()
    colorYellow.setStroke()
    let r1 = NSBezierPath(ovalIn: NSRect(x: 240, y: 640, width: 70, height: 70))
    let r2 = NSBezierPath(ovalIn: NSRect(x: 280, y: 620, width: 70, height: 70))
    r1.lineWidth = 10; r2.lineWidth = 10
    r1.stroke(); r2.stroke()
    // Connector line to timeline
    colorCoral.setStroke()
    let line1 = NSBezierPath()
    line1.lineWidth = 4; line1.move(to: NSPoint(x: 310, y: 780)); line1.line(to: NSPoint(x: 310, y: 880)); line1.stroke()
    ctx.cgContext.restoreGState()
    
    // 2. Business at 27 (Center top)
    let stamp2Rect = NSRect(x: 480, y: 1140, width: 220, height: 260)
    drawTornPaperCard(rect: stamp2Rect, fillColor: colorNavyDark)
    // Shop / storefront icon
    colorYellow.setFill()
    let roof2 = NSBezierPath()
    roof2.move(to: NSPoint(x: 590, y: 1340))
    roof2.line(to: NSPoint(x: 660, y: 1280))
    roof2.line(to: NSPoint(x: 520, y: 1280))
    roof2.close(); roof2.fill()
    colorCream.setFill()
    NSBezierPath(rect: NSRect(x: 535, y: 1190, width: 110, height: 90)).fill()
    // Connector line to timeline
    colorNavy.setStroke()
    let line2 = NSBezierPath()
    line2.lineWidth = 4; line2.move(to: NSPoint(x: 590, y: 1140)); line2.line(to: NSPoint(x: 590, y: 1040)); line2.stroke()
    
    // 3. Degree at 29 (Right top)
    let stamp3Rect = NSRect(x: 740, y: 1160, width: 220, height: 260)
    drawTornPaperCard(rect: stamp3Rect, fillColor: colorCoral)
    // Rolled diploma icon with ribbon
    colorCream.setFill()
    NSBezierPath(roundedRect: NSRect(x: 780, y: 1260, width: 140, height: 60), xRadius: 12, yRadius: 12).fill()
    colorYellow.setFill()
    NSBezierPath(rect: NSRect(x: 835, y: 1245, width: 30, height: 90)).fill()
    // Connector line to timeline
    colorCoral.setStroke()
    let line3 = NSBezierPath()
    line3.lineWidth = 4; line3.move(to: NSPoint(x: 850, y: 1160)); line3.line(to: NSPoint(x: 850, y: 1040)); line3.stroke()
    
    // Tape pieces
    drawTape(at: NSPoint(x: 100, y: 960), width: 140, height: 48, angleDeg: 90)
    drawTape(at: NSPoint(x: 980, y: 960), width: 140, height: 48, angleDeg: 90)
    
    saveJPEG(rep, "beat06_poster.jpg")
}

// MARK: - Beat 7: Two Races (Sprinter on Blocks & Marathoner with Water Cup)
func renderBeat07() {
    let (rep, ctx) = createCanvas()
    drawPaperBackground(ctx: ctx.cgContext)
    
    // Halftone accent on right
    drawHalftoneGrid(rect: NSRect(x: 540, y: 200, width: 500, height: 1520), dotColor: colorCoral.withAlphaComponent(0.18), dotSpacing: 20, dotRadius: 3.5)
    
    // Running track perspective lanes
    ctx.cgContext.saveGState()
    colorNavy.setStroke()
    for i in 0...4 {
        let path = NSBezierPath()
        path.lineWidth = 4.0
        path.move(to: NSPoint(x: 80 + CGFloat(i) * 230, y: 80))
        path.line(to: NSPoint(x: 320 + CGFloat(i) * 110, y: 1840))
        path.stroke()
    }
    ctx.cgContext.restoreGState()
    
    // Beat 7 Background: Clean running track with subtle lane markers and texture
    // (Human runner cards animate dynamically on top via HyperFrames)
    
    // Tape pieces
    drawTape(at: NSPoint(x: 320, y: 1040), width: 140, height: 44, angleDeg: 15)
    drawTape(at: NSPoint(x: 760, y: 1540), width: 140, height: 44, angleDeg: -20)
    drawTape(at: NSPoint(x: 120, y: 1800), width: 130, height: 44, angleDeg: 35)
    drawTape(at: NSPoint(x: 960, y: 1800), width: 130, height: 44, angleDeg: -35)
    
    saveJPEG(rep, "beat07_poster.jpg")
}

// MARK: - Beat 8: The Fair Scoreboard (Two Columns: You Last Year vs You Now)
func renderBeat08() {
    let (rep, ctx) = createCanvas()
    drawPaperBackground(ctx: ctx.cgContext)
    
    // Two-Column Scoreboard Card on cream
    let boardRect = NSRect(x: 80, y: 340, width: 920, height: 1280)
    drawTornPaperCard(rect: boardRect, fillColor: colorCreamDark)
    
    // Column 1 (Left): YOU — LAST YEAR (Faded, desaturated, halftone)
    let col1Rect = NSRect(x: 130, y: 460, width: 380, height: 1060)
    drawTornPaperCard(rect: col1Rect, fillColor: colorNavy.withAlphaComponent(0.25))
    // Halftone inside faded column
    drawHalftoneGrid(rect: col1Rect.insetBy(dx: 20, dy: 20), dotColor: colorNavy.withAlphaComponent(0.35), dotSpacing: 16, dotRadius: 3.0)
    // Faded runner silhouette
    colorNavy.withAlphaComponent(0.40).setFill()
    let fHead = NSBezierPath(ovalIn: NSRect(x: 275, y: 1160, width: 90, height: 90))
    let fTorso = NSBezierPath(roundedRect: NSRect(x: 260, y: 840, width: 120, height: 300), xRadius: 24, yRadius: 24)
    fHead.fill(); fTorso.fill()
    
    // Column 2 (Right): YOU — NOW (Vibrant, saturated full-color coral & yellow)
    let col2Rect = NSRect(x: 570, y: 460, width: 380, height: 1060)
    drawTornPaperCard(rect: col2Rect, fillColor: colorCoral)
    // Vibrant runner silhouette
    colorYellow.setFill()
    let vHead = NSBezierPath(ovalIn: NSRect(x: 715, y: 1160, width: 90, height: 90))
    vHead.fill()
    colorCream.setFill()
    let vTorso = NSBezierPath(roundedRect: NSRect(x: 700, y: 840, width: 120, height: 300), xRadius: 24, yRadius: 24)
    vTorso.fill()
    // Golden star emblem
    colorYellow.setFill()
    NSBezierPath(ovalIn: NSRect(x: 740, y: 960, width: 40, height: 40)).fill()
    
    // Hand-drawn yellow marker circle/oval around both columns
    ctx.cgContext.saveGState()
    colorYellow.setStroke()
    let circle = NSBezierPath(ovalIn: NSRect(x: 100, y: 400, width: 880, height: 1160))
    circle.lineWidth = 14.0
    circle.stroke()
    ctx.cgContext.restoreGState()
    
    // Tape pieces
    drawTape(at: NSPoint(x: 180, y: 1620), width: 140, height: 44, angleDeg: -30)
    drawTape(at: NSPoint(x: 900, y: 1620), width: 140, height: 44, angleDeg: 30)
    drawTape(at: NSPoint(x: 540, y: 320), width: 160, height: 44, angleDeg: 0)
    
    saveJPEG(rep, "beat08_poster.jpg")
}

// MARK: - Beat 9: Closer (Serene Track, One Runner, Morning Light)
func renderBeat09() {
    let (rep, ctx) = createCanvas()
    drawPaperBackground(ctx: ctx.cgContext)
    
    // Warm morning-light flat color shift glow near top horizon
    ctx.cgContext.saveGState()
    let glowRect = NSRect(x: 60, y: 1200, width: 960, height: 640)
    drawTornPaperCard(rect: glowRect, fillColor: colorCoral.withAlphaComponent(0.20))
    
    // Halftone dots morning gradient
    drawHalftoneGrid(rect: glowRect.insetBy(dx: 20, dy: 20), dotColor: colorYellow.withAlphaComponent(0.35), dotSpacing: 18, dotRadius: 3.5)
    ctx.cgContext.restoreGState()
    
    // Running track drawn on cream paper receding toward horizon
    ctx.cgContext.saveGState()
    colorNavy.setStroke()
    for i in 0...4 {
        let path = NSBezierPath()
        path.lineWidth = 4.5
        path.move(to: NSPoint(x: 100 + CGFloat(i) * 220, y: 80))
        path.line(to: NSPoint(x: 360 + CGFloat(i) * 90, y: 1720))
        path.stroke()
    }
    
    // Golden finish line ahead in distance
    colorYellow.setFill()
    NSRect(x: 340, y: 1680, width: 400, height: 18).fill()
    
    // ONE single runner mid-track in full confident stride heading toward horizon
    let rx: CGFloat = 540
    // Beat 9 Background: Clean morning-light perspective track
    // (Human runner animates dynamically on top via HyperFrames)
    ctx.cgContext.restoreGState()
    
    // Tape pieces
    drawTape(at: NSPoint(x: 140, y: 1840), width: 140, height: 44, angleDeg: 35)
    drawTape(at: NSPoint(x: 940, y: 1840), width: 140, height: 44, angleDeg: -35)
    drawTape(at: NSPoint(x: 540, y: 100), width: 160, height: 44, angleDeg: 0)
    
    saveJPEG(rep, "beat09_poster.jpg")
}

// MARK: - Execute All Posters
print("Starting generation of Beats 02–09 in Theme A (Classic Vox)...")
renderBeat02()
renderBeat03()
renderBeat04()
renderBeat05()
renderBeat06()
renderBeat07()
renderBeat08()
renderBeat09()
print("All 8 posters generated successfully!")
