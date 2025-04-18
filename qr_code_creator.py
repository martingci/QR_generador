from PIL import Image, ImageDraw
import qrcode

def create_qrcode(link, filename):
    # Crea el codigo qr
    qr = qrcode.QRCode(
        version=1, 
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=150, 
        border=1)

    # añade la info
    qr.add_data(link)

    # crea el codigo
    qr.make(fit=True)

    # crea la imagen con colores
    img = qr.make_image(fill_color="#134797", back_color="white").convert("RGBA")
    print(img.size)

    # abre el logo
    logo = Image.open("logo.png").convert("RGBA")

    size = int(img.size[0]*0.3) #lo transforma respecto al tamaño del código qr

    # lo cambia de tamaño
    logo = logo.resize((size, size))

    # lo hace más pequeño para que encaje mejor
    smaller_logo_size = (int(size * 0.9), int(size * 0.9)) 
    logo_smaller = logo.resize(smaller_logo_size)

    # crea un logo nuevo con forma circular
    logo_with_padding = Image.new("RGBA", logo.size, "WHITE")

    # centra el logo con menor tamaño
    offset = ((logo_with_padding.size[0] - logo_smaller.size[0]) // 2,
            (logo_with_padding.size[1] - logo_smaller.size[1]) // 2)
    logo_with_padding.paste(logo_smaller, offset, mask=logo_smaller)

    # crea una mascara de circulo
    mask = Image.new("L", logo.size, 0) 
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, logo.size[0], logo.size[1]), fill=255)  # lo realiza

    # aplica el circulo a la imagen rescalada
    logo_circular = Image.new("RGBA", logo.size)
    logo_circular.paste(logo_with_padding, (0, 0), mask=mask)

    # centra la imagen
    img_w, img_h = img.size
    logo_w, logo_h = logo_circular.size
    pos = ((img_w - logo_w) // 2, (img_h - logo_h) // 2)

    # copia el logo rescalado al qr
    img.paste(logo_circular, pos, mask=logo_circular)

    # lo exporta a un nombre proporcionado por el usuario
    img.save(filename+".png")
