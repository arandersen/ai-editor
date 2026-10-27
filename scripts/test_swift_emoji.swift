import Cocoa

let width = 1080
let height = 1920

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

func drawBeanBoozleTitle(text: String, rect: NSRect, fontSize: CGFloat) {
    let font = NSFont(name: "Arial-Black", size: fontSize) ?? NSFont.systemFont(ofSize: fontSize, weight: .black)
    let pCenter = NSMutableParagraphStyle()
    pCenter.alignment = .center
    pCenter.lineBreakMode = .byClipping

    let sh = NSShadow()
    sh.shadowColor = NSColor(calibratedWhite: 0.0, alpha: 0.85)
    sh.shadowBlurRadius = 8.0
    sh.shadowOffset = NSSize(width: 0, height: -4)

    // Base pass: outline
    let p1: [NSAttributedString.Key: Any] = [
        .font: font,
        .foregroundColor: NSColor.black,
        .strokeColor: NSColor.black,
        .strokeWidth: -4.0,
        .shadow: sh,
        .paragraphStyle: pCenter
    ]
    NSAttributedString(string: text, attributes: p1).draw(in: rect)

    // Top pass: white fill
    let p2: [NSAttributedString.Key: Any] = [
        .font: font,
        .foregroundColor: NSColor.white,
        .paragraphStyle: pCenter
    ]
    NSAttributedString(string: text, attributes: p2).draw(in: rect)
}

let (rep, _) = createCanvas()
drawBeanBoozleTitle(text: "KARTU PASANGAN 🔥", rect: NSRect(x: 10, y: 1560, width: 1060, height: 160), fontSize: 74)

let url = URL(fileURLWithPath: "broll/Kartu Pasangan/test_hook_emoji.png")
let pngData = rep.representation(using: .png, properties: [:])!
try! pngData.write(to: url)
print("Saved test_hook_emoji.png at 74pt")
