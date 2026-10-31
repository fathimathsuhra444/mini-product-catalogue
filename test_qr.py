import qrcode

upi_id = "yourupiid@upi"
amount = "100.00"

upi_url = (
    f"upi://pay?pa={upi_id}"
    f"&pn=MiniCatalogue"
    f"&am={amount}"
    f"&cu=INR"
)

qr = qrcode.make(upi_url)
qr.save("upi_qr.png")

print("UPI QR code created successfully!")