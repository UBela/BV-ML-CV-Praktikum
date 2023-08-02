import customtkinter
from UI import App


app_instance = App()

app_instance.mainloop()

app_instance.upload_image_to_database("TestImagesSet1\image_1.jpg", True, "SHG-FF-206")
