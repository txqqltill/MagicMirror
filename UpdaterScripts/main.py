from core.app import App
import data.loacations as locations

if __name__ == "__main__":
    app = App(locations.image_path)
    app.run()
