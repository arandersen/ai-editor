import Cocoa

let width = 2160
let height = 3840
let outDir = "/Users/arthurandersen/Documents/AI_Video_Editor_Gemini/broll/Tebak Snack"

try? FileManager.default.createDirectory(atPath: outDir, withIntermediateDirectories: true, attributes: nil)

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

func savePNG(_ rep: NSBitmapImageRep, _ filename: String) {
    let url = URL(fileURLWithPath: "\(outDir)/\(filename)")
    let pngData = rep.representation(using: .png, properties: [:])!
    try! pngData.write(to: url)
    print("Saved 4K: \(filename)")
}

// Draw top header with separate text (Arial Black, white fill, black stroke)
// and emoji (AppleColorEmoji, full color, no stroke) in native 4K
func drawHeaderWithEmoji(text: String, emoji: String, rect: NSRect, fontSize: CGFloat, emojiSize: CGFloat) {
    var fSize = fontSize
    var eSize = emojiSize
    
    func buildString(f: CGFloat, e: CGFloat) -> NSMutableAttributedString {
        let res = NSMutableAttributedString()
        let fontText = NSFont(name: "Arial-Black", size: f) ?? NSFont.systemFont(ofSize: f, weight: .black)
        let fontEmoji = NSFont(name: "AppleColorEmoji", size: e) ?? NSFont.systemFont(ofSize: e)
        let sh = NSShadow()
        sh.shadowColor = NSColor(calibratedWhite: 0.0, alpha: 0.85)
        sh.shadowBlurRadius = 16.0
        sh.shadowOffset = NSSize(width: 0, height: -8)
        let pCenter = NSMutableParagraphStyle()
        pCenter.alignment = .center
        
        let textAttrs: [NSAttributedString.Key: Any] = [
            .font: fontText,
            .foregroundColor: NSColor.white,
            .strokeColor: NSColor.black,
            .strokeWidth: -7.5,
            .shadow: sh,
            .paragraphStyle: pCenter
        ]
        res.append(NSAttributedString(string: text, attributes: textAttrs))
        if !emoji.isEmpty {
            let emojiAttrs: [NSAttributedString.Key: Any] = [
                .font: fontEmoji,
                .shadow: sh,
                .paragraphStyle: pCenter
            ]
            res.append(NSAttributedString(string: " " + emoji, attributes: emojiAttrs))
        }
        return res
    }
    
    var astr = buildString(f: fSize, e: eSize)
    while astr.size().width > rect.width - 120 && fSize > 50 {
        fSize -= 3
        eSize -= 3
        astr = buildString(f: fSize, e: eSize)
    }
    
    astr.draw(in: rect)
}

// Draw hook title: 'challenge' + 'TEBAK SNACK PASANGAN 🛒' in native 4K
func drawHook() {
    let (rep, _) = createCanvas()
    let pCenter = NSMutableParagraphStyle()
    pCenter.alignment = .center

    // Line 1: 'challenge' (HelveticaNeue-Bold, 136pt, black fill with white stroke)
    let fontSub = NSFont(name: "HelveticaNeue-Bold", size: 136) ?? NSFont.systemFont(ofSize: 136, weight: .bold)
    let sh1 = NSShadow()
    sh1.shadowColor = NSColor(calibratedWhite: 0.0, alpha: 0.55)
    sh1.shadowBlurRadius = 16.0
    sh1.shadowOffset = NSSize(width: 0, height: -6)

    let p1: [NSAttributedString.Key: Any] = [
        .font: fontSub,
        .foregroundColor: NSColor.white,
        .strokeColor: NSColor.white,
        .strokeWidth: -30.0,
        .shadow: sh1,
        .paragraphStyle: pCenter
    ]
    NSAttributedString(string: "challenge", attributes: p1).draw(in: NSRect(x: 80, y: 3380, width: 2000, height: 190))

    let p2: [NSAttributedString.Key: Any] = [
        .font: fontSub,
        .foregroundColor: NSColor.black,
        .paragraphStyle: pCenter
    ]
    NSAttributedString(string: "challenge", attributes: p2).draw(in: NSRect(x: 80, y: 3380, width: 2000, height: 190))

    // Line 2: 'TEBAK SNACK PASANGAN 🛒'
    drawHeaderWithEmoji(text: "TEBAK SNACK PASANGAN", emoji: "🛒", rect: NSRect(x: 20, y: 3120, width: 2120, height: 320), fontSize: 132, emojiSize: 132)
    savePNG(rep, "hook_tebak_snack.png")
}

drawHook()

struct HeaderItem {
    let filename: String
    let text: String
    let emoji: String
}

let headers: [HeaderItem] = [
    HeaderItem(filename: "header_r1_title.png", text: "ROUND 1: TEBAK SNACK", emoji: "🍟"),
    HeaderItem(filename: "header_r1_arthur_fail.png", text: "ARTHUR: PRINGLES (ANGEL: LAY'S)", emoji: "❌🥔"),
    HeaderItem(filename: "header_r1_angel_fail.png", text: "ANGEL: YOGURT RAISINS (ARTHUR: PRINGLES)", emoji: "❌🍇"),
    HeaderItem(filename: "header_r1_score.png", text: "SKOR: 0 — 0 (GAK ADA YANG BENER!)", emoji: "😅"),
    HeaderItem(filename: "header_r2_title.png", text: "ROUND 2: TEBAK COKELAT", emoji: "🍫"),
    HeaderItem(filename: "header_r2_angel_correct.png", text: "ANGEL: BROOKSIDE BERRY! BENAR!", emoji: "✅🫐✨"),
    HeaderItem(filename: "header_r2_arthur_fail.png", text: "ARTHUR: BROOKSIDE (ANGEL: FERRERO)", emoji: "❌🍫"),
    HeaderItem(filename: "header_r2_score.png", text: "ANGEL MEMIMPIN: 1 — 0!", emoji: "👏🔥"),
    HeaderItem(filename: "header_r3_title.png", text: "ROUND 3: TEBAK ES KRIM", emoji: "🍦"),
    HeaderItem(filename: "header_r3_arthur_correct.png", text: "ARTHUR: HAAGEN-DAZS MATCHA! BENAR!", emoji: "✅🍵"),
    HeaderItem(filename: "header_r3_angel_correct.png", text: "ANGEL: TALENTI MANGO! BENAR!", emoji: "✅🥭"),
    HeaderItem(filename: "header_r3_both_correct.png", text: "DUA-DUANYA BENAR!", emoji: "🍦✨🎉"),
    HeaderItem(filename: "header_r3_score.png", text: "SKOR: ANGEL 2 — 1 ARTHUR", emoji: "👏"),
    HeaderItem(filename: "header_r4_title.png", text: "ROUND 4: TEBAK MINUMAN", emoji: "🧃"),
    HeaderItem(filename: "header_r4_arthur_fail.png", text: "ARTHUR: APPLE CIDER (ANGEL: YAKULT)", emoji: "❌🍎"),
    HeaderItem(filename: "header_r4_angel_fail.png", text: "ANGEL: SUSU OATLY (ARTHUR: TEH)", emoji: "❌🥛"),
    HeaderItem(filename: "header_winner.png", text: "ANGEL MENANG! ARTHUR BELI SEMUA!", emoji: "🏆🛒🎉")
]

for h in headers {
    let (rep, _) = createCanvas()
    drawHeaderWithEmoji(text: h.text, emoji: h.emoji, rect: NSRect(x: 40, y: 3220, width: 2080, height: 320), fontSize: 120, emojiSize: 120)
    savePNG(rep, h.filename)
}

print("All 4K Tebak Snack headers generated successfully!")
