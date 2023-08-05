from IPython.display import Audio, display


class InvisibleAudio(Audio):
    def __init__(self, path: str):
        super().__init__(
            filename=path,
            autoplay=True
        )

    def _repr_html_(self):
        audio = super()._repr_html_()
        audio = audio.replace(
            '<audio', '<audio onended="this.parentNode.removeChild(this)"')
        return '<div style="display:none">{audio}</div>'.format(
            audio=audio
        )

    def play(self):
        display(self)
