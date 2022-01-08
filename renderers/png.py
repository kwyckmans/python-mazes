from PIL import Image, ImageDraw

img = Image.new('RGB', (250, 250), color = 'green')
img.save('pil_red.png')


WHITE = (255,255,255)

class PNGExporter():
    def render(self) -> None:
        image = self._render(200,200)
        image.save("render_test.png","PNG", optimize=True)

    def _render(self, width: int, height: int) -> Image.Image:
        image = Image.new("RGBA", (width + 1, height + 1), WHITE)
        draw = ImageDraw.Draw(image)

        for i in range(1,width, 10):
            draw.rectangle((i, i, i + 10, i + 10), fill=(255 % i,255 % i,255 % i))

        return image


if __name__ == "__main__":
    exporter = PNGExporter()

    exporter.render()
