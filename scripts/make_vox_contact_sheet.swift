import Cocoa

let cellW = 540
let cellH = 960
let cols = 3
let rows = 3
let sheetW = cols * cellW
let sheetH = rows * cellH

let baseDir = "/Users/arthurandersen/Documents/AI_Video_Editor_Gemini/VOX-TEST_race/01_storyboard"
let postersDir = "\(baseDir)/posters"
let outFile = "\(baseDir)/contact-sheet.jpg"

let beats: [(Int, String, String)] = [
    (1, "0:00–0:06", "beat01_poster.jpg"),
    (2, "0:06–0:13", "beat02_poster.jpg"),
    (3, "0:13–0:20", "beat03_poster.jpg"),
    (4, "0:20–0:27", "beat04_poster.jpg"),
    (5, "0:27–0:34", "beat05_poster.jpg"),
    (6, "0:34–0:42", "beat06_poster.jpg"),
    (7, "0:42–0:49", "beat07_poster.jpg"),
    (8, "0:49–0:55", "beat08_poster.jpg"),
    (9, "0:55–1:00", "beat09_poster.jpg")
]

let rep = NSBitmapImageRep(
    bitmapDataPlanes: nil,
    pixelsWide: sheetW,
    pixelsHigh: sheetH,
    bitsPerSample: 8,
    samplesPerPixel: 4,
    hasAlpha: true,
    isPlanar: false,
    colorSpaceName: .deviceRGB,
    bytesPerRow: sheetW * 4,
    bitsPerPixel: 32
)!
let ctx = NSGraphicsContext(bitmapImageRep: rep)!
NSGraphicsContext.current = ctx

// Fill background dark slate
NSColor(calibratedRed: 0.08, green: 0.10, blue: 0.14, alpha: 1.0).setFill()
NSRect(x: 0, y: 0, width: sheetW, height: sheetH).fill()

for (idx, (beatNum, timeRange, filename)) in beats.enumerated() {
    let col = idx % cols
    let row = idx / cols
    let x = CGFloat(col * cellW)
    let y = CGFloat((rows - 1 - row) * cellH) // Invert Y for Cocoa
    let cellRect = NSRect(x: x, y: y, width: CGFloat(cellW), height: CGFloat(cellH))
    
    let imgPath = "\(postersDir)/\(filename)"
    if let img = NSImage(contentsOfFile: imgPath) {
        img.draw(in: cellRect)
    }
    
    // Draw thin cell border
    NSColor(calibratedWhite: 1.0, alpha: 0.15).setStroke()
    let border = NSBezierPath(rect: cellRect)
    border.lineWidth = 2.0
    border.stroke()
    
    // Draw badge pill top-left of each cell
    let badgeRect = NSRect(x: x + 24, y: y + CGFloat(cellH) - 64, width: 260, height: 42)
    let badgePath = NSBezierPath(roundedRect: badgeRect, xRadius: 10, yRadius: 10)
    NSColor(calibratedRed: 0.08, green: 0.10, blue: 0.14, alpha: 0.88).setFill()
    badgePath.fill()
    NSColor(calibratedRed: 1.0, green: 0.835, blue: 0.122, alpha: 0.85).setStroke()
    badgePath.lineWidth = 1.5
    badgePath.stroke()
    
    // Badge text: "BEAT X (0:XX–0:XX)"
    let text = "BEAT \(beatNum)  (\(timeRange))"
    let pCenter = NSMutableParagraphStyle()
    pCenter.alignment = .center
    let font = NSFont(name: "Arial-Bold", size: 18) ?? NSFont.boldSystemFont(ofSize: 18)
    let attrs: [NSAttributedString.Key: Any] = [
        .font: font,
        .foregroundColor: NSColor.white,
        .paragraphStyle: pCenter
    ]
    let astr = NSAttributedString(string: text, attributes: attrs)
    astr.draw(in: NSRect(x: badgeRect.minX, y: badgeRect.minY + 8, width: badgeRect.width, height: 26))
}

let outUrl = URL(fileURLWithPath: outFile)
let data = rep.representation(using: .jpeg, properties: [.compressionFactor: 0.90])!
try! data.write(to: outUrl)
print("Saved 3x3 contact sheet to \(outFile) (\(data.count) bytes)")
