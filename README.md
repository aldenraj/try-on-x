# 👗 Virtual Try-On Application

A web-based virtual try-on application that allows users to visualize how garments look on people using AI-powered image generation. Built with Gradio and powered by the OOTDiffusion model.

## 🌟 Features

- **Easy-to-use Web Interface**: Upload images through an intuitive web UI
- **High-Quality Results**: Uses OOTDiffusion model for realistic try-on results
- **Customizable Parameters**: Adjust generation settings for optimal results
- **Multiple Output Images**: Generate multiple variations in one go
- **Real-time Progress**: Track the processing status with progress indicators
- **Clean Design**: Modern, responsive interface that works on all devices

## 📋 Prerequisites

- Python 3.8 or higher
- Internet connection (for API calls)
- Modern web browser

## 🚀 Installation

1. **Clone or navigate to the project directory:**

   ```powershell
   cd "c:\Users\John Abish\NPC_Data_Marketplace\Azure_Unifi_Org_Git\Tryon"
   ```

2. **Create a virtual environment (recommended):**

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install required packages:**
   ```powershell
   pip install -r requirements.txt
   ```

## 🎯 Usage

1. **Start the application:**

   ```powershell
   python app_new.py
   ```

2. **Open your browser:**

   - The application will automatically open in your default browser
   - Or manually navigate to: `http://localhost:7860`

3. **Use the application:**
   - Upload a **Model Image** (person's photo)
   - Upload a **Garment Image** (clothing item)
   - Adjust parameters if needed (optional)
   - Click **"Generate Try-On"**
   - Wait for the results to appear

## 🎨 Parameters Explained

| Parameter            | Description                             | Recommended Value       |
| -------------------- | --------------------------------------- | ----------------------- |
| **Number of Images** | How many variations to generate         | 1-2 (more takes longer) |
| **Steps**            | Quality of generation (higher = better) | 20-30                   |
| **Guidance Scale**   | How closely to follow the garment       | 2.0                     |
| **Seed**             | For reproducible results                | -1 (random)             |

## 💡 Tips for Best Results

1. **Model Image (Person):**

   - Use clear, well-lit photos
   - Full-body shots work best
   - Person should face forward
   - Neutral pose recommended
   - Avoid busy backgrounds

2. **Garment Image:**

   - Clean, white or simple background
   - Garment should be clearly visible
   - Good lighting and focus
   - Front view of the garment

3. **Parameters:**
   - Start with default settings
   - Increase steps (30-40) for better quality
   - Try different seeds if unsatisfied
   - Use 1 sample first, then increase if needed

## 📁 Project Structure

```
Tryon/
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## 🔧 Advanced Configuration

### Change Port

Edit the `app.py` file and modify the `server_port` parameter:

```python
demo.launch(server_port=8080)  # Change to your desired port
```

### Create Public Link

Set `share=True` in the launch configuration:

```python
demo.launch(share=True)  # Creates a temporary public URL
```

### Run in Background

```powershell
Start-Process python -ArgumentList "app.py" -WindowStyle Hidden
```

## 🐛 Troubleshooting

### Issue: "Module not found" error

**Solution:** Make sure you've installed all requirements:

```powershell
pip install -r requirements.txt
```

### Issue: Application won't start

**Solution:** Check if port 7860 is available:

```powershell
netstat -ano | findstr :7860
```

### Issue: API errors

**Solution:**

- Check your internet connection
- The OOTDiffusion API might be temporarily unavailable
- Try again after a few minutes

### Issue: Poor quality results

**Solution:**

- Use higher quality input images
- Increase the "Steps" parameter
- Try different model or garment images

## 📝 API Information

This application uses the **OOTDiffusion** API hosted on Hugging Face:

- Model: `levihsu/OOTDiffusion`
- API Endpoint: `/process_hd`
- Documentation: [Hugging Face Space](https://huggingface.co/spaces/levihsu/OOTDiffusion)

## 🔒 Privacy Note

- Images are processed through the OOTDiffusion API
- No images are stored permanently by this application
- Temporary files are handled by the system's temp directory
- Please review the OOTDiffusion model's privacy policy for API usage

## 📄 License

This project is provided as-is for educational and personal use.

## 🤝 Contributing

Feel free to fork, modify, and enhance this application for your needs!

## 📧 Support

For issues or questions:

1. Check the Troubleshooting section above
2. Review the OOTDiffusion documentation
3. Ensure all dependencies are correctly installed

## 🎉 Acknowledgments

- **OOTDiffusion** team for the amazing model
- **Gradio** for the easy-to-use interface framework
- **Hugging Face** for hosting the API

---

**Happy Try-On! 👔👗👕**
