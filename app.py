"""
Virtual Try-On Application using OOTDiffusion API
This application allows users to virtually try on garments by uploading images.
"""

import gradio as gr
from gradio_client import Client, handle_file
import os
import tempfile
from pathlib import Path
from typing import List, Tuple, Optional
import time


class VirtualTryOnApp:
    """Main application class for virtual try-on functionality"""
    
    def __init__(self):
        """Initialize the Virtual Try-On application"""
        self.client = Client("levihsu/OOTDiffusion")
        self.temp_dir = tempfile.gettempdir()
        
    def process_tryon(
        self,
        model_image: str,
        garment_image: str,
        num_samples: int = 1,
        num_steps: int = 20,
        guidance_scale: float = 2.0,
        seed: int = -1,
        progress=gr.Progress()
    ) -> Tuple[List, str]:
        """
        Process virtual try-on using the OOTDiffusion API
        
        Args:
            model_image: Path to the model/person image
            garment_image: Path to the garment image
            num_samples: Number of output images to generate
            num_steps: Number of diffusion steps
            guidance_scale: Guidance scale for generation
            seed: Random seed (-1 for random)
            
        Returns:
            Tuple of (list of output images, status message)
        """
        try:
            # Validate inputs
            if model_image is None:
                return None, "❌ Error: Please upload a model image"
            if garment_image is None:
                return None, "❌ Error: Please upload a garment image"
            
            progress(0.1, desc="✨ Uploading images...")
            
            # Call the API
            progress(0.3, desc="🎨 Processing virtual try-on...")
            result = self.client.predict(
                vton_img=handle_file(model_image),
                garm_img=handle_file(garment_image),
                n_samples=int(num_samples),
                n_steps=int(num_steps),
                image_scale=float(guidance_scale),
                seed=int(seed),
                api_name="/process_hd"
            )
            
            progress(0.9, desc="✨ Finalizing your look...")
            
            # Process results
            # The API returns a list of dictionaries with 'image' and 'caption' keys
            print(f"API Response type: {type(result)}")
            print(f"API Response: {result}")
            
            if result:
                output_images = []
                
                # Handle different response formats
                if isinstance(result, list):
                    for item in result:
                        if isinstance(item, dict):
                            # Extract the image path from dict
                            if 'image' in item:
                                img_path = item['image']
                                # Handle both string paths and dict with path
                                if isinstance(img_path, dict) and 'path' in img_path:
                                    output_images.append(img_path['path'])
                                elif isinstance(img_path, str):
                                    output_images.append(img_path)
                        elif isinstance(item, str):
                            # Direct image path
                            output_images.append(item)
                elif isinstance(result, dict) and 'image' in result:
                    # Single image result
                    img_path = result['image']
                    if isinstance(img_path, dict) and 'path' in img_path:
                        output_images.append(img_path['path'])
                    elif isinstance(img_path, str):
                        output_images.append(img_path)
                elif isinstance(result, str):
                    # Direct path
                    output_images.append(result)
                
                if output_images:
                    progress(1.0, desc="Complete!")
                    return output_images, f"✅ Successfully generated {len(output_images)} image(s)!"
                else:
                    return None, f"⚠️ No images found in result. Response format: {type(result)}"
            else:
                return None, "⚠️ Empty response from API. Please try again."
                
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            error_msg = f"❌ Error during processing: {str(e)}\n\nDetails:\n{error_details}"
            print(error_msg)
            return None, f"❌ Error: {str(e)}"
    
    def clear_inputs(self):
        """Clear all inputs"""
        return None, None, 1, 20, 2.0, -1, None, ""


def create_interface():
    """Create and configure the Gradio interface"""
    
    app = VirtualTryOnApp()
    
    # Premium Custom CSS - Luxurious Design
    custom_css = """
    /* Import Premium Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    :root {
        --primary-color: #1e40af;
        --primary-light: #3b82f6;
        --accent-gold: #d4af37;
        --accent-emerald: #10b981;
        --neutral-50: #fafaf9;
        --neutral-100: #f5f5f4;
        --neutral-200: #e7e5e4;
        --neutral-800: #292524;
        --neutral-900: #1c1917;
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
        --gradient-elegant: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --gradient-gold: linear-gradient(135deg, #f6d365 0%, #fda085 100%);
        --gradient-emerald: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
    }
    
    * {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    /* Main Container */
    .gradio-container {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background: linear-gradient(to bottom, #fafaf9 0%, #f5f5f4 100%) !important;
        max-width: 1400px !important;
        margin: 0 auto !important;
        padding: 0 !important;
    }
    
    /* Navbar Styles */
    .app-navbar {
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(10px) !important;
        border-bottom: 1px solid var(--neutral-200) !important;
        padding: 1.5rem 3rem !important;
        position: sticky !important;
        top: 0 !important;
        z-index: 1000 !important;
        box-shadow: var(--shadow-sm) !important;
    }
    
    .app-logo {
        font-family: 'Playfair Display', serif !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
        background: var(--gradient-elegant) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        letter-spacing: -0.02em !important;
    }
    
    /* Hero Section */
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        padding: 5rem 3rem !important;
        text-align: center !important;
        border-radius: 0 0 3rem 3rem !important;
        margin-bottom: 4rem !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .hero-section::before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        bottom: 0 !important;
        background: url('data:image/svg+xml,<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg"><defs><pattern id="grid" width="100" height="100" patternUnits="userSpaceOnUse"><path d="M 100 0 L 0 0 0 100" fill="none" stroke="white" stroke-width="0.5" opacity="0.1"/></pattern></defs><rect width="100%" height="100%" fill="url(%23grid)"/></svg>') !important;
        opacity: 0.3 !important;
    }
    
    .hero-title {
        font-family: 'Playfair Display', serif !important;
        font-size: 3.5rem !important;
        font-weight: 700 !important;
        color: white !important;
        margin-bottom: 1.5rem !important;
        line-height: 1.2 !important;
        letter-spacing: -0.02em !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
        position: relative !important;
        z-index: 1 !important;
    }
    
    .hero-subtitle {
        font-size: 1.25rem !important;
        color: rgba(255, 255, 255, 0.95) !important;
        margin-bottom: 2.5rem !important;
        font-weight: 300 !important;
        max-width: 600px !important;
        margin-left: auto !important;
        margin-right: auto !important;
        position: relative !important;
        z-index: 1 !important;
    }
    
    /* Section Headers */
    .section-header {
        font-family: 'Playfair Display', serif !important;
        font-size: 2.5rem !important;
        font-weight: 600 !important;
        color: var(--neutral-900) !important;
        text-align: center !important;
        margin-bottom: 1rem !important;
        letter-spacing: -0.02em !important;
    }
    
    .section-subtitle {
        font-size: 1.1rem !important;
        color: #78716c !important;
        text-align: center !important;
        margin-bottom: 3rem !important;
        font-weight: 400 !important;
    }
    
    /* Upload Areas */
    .upload-card {
        background: white !important;
        border-radius: 1.5rem !important;
        padding: 2.5rem !important;
        box-shadow: var(--shadow-lg) !important;
        border: 2px solid transparent !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .upload-card::before {
        content: '' !important;
        position: absolute !important;
        inset: 0 !important;
        border-radius: 1.5rem !important;
        padding: 2px !important;
        background: var(--gradient-elegant) !important;
        -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0) !important;
        -webkit-mask-composite: xor !important;
        mask-composite: exclude !important;
        opacity: 0 !important;
        transition: opacity 0.4s !important;
    }
    
    .upload-card:hover {
        transform: translateY(-4px) !important;
        box-shadow: var(--shadow-xl) !important;
    }
    
    .upload-card:hover::before {
        opacity: 1 !important;
    }
    
    /* Image Upload Zones */
    [data-testid="image"] {
        border-radius: 1rem !important;
        border: 2px dashed var(--neutral-300) !important;
        background: var(--neutral-50) !important;
        transition: all 0.3s ease !important;
        min-height: 300px !important;
    }
    
    [data-testid="image"]:hover {
        border-color: var(--primary-color) !important;
        background: white !important;
        box-shadow: inset 0 0 0 1px var(--primary-color) !important;
    }
    
    /* Labels & Text */
    label {
        font-weight: 600 !important;
        color: var(--neutral-800) !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.01em !important;
        margin-bottom: 0.75rem !important;
    }
    
    /* Buttons */
    .primary-button, button[variant="primary"] {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-light) 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 0.75rem !important;
        padding: 1rem 2.5rem !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        box-shadow: var(--shadow-md) !important;
        cursor: pointer !important;
        letter-spacing: 0.02em !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .primary-button::before {
        content: '' !important;
        position: absolute !important;
        top: 50% !important;
        left: 50% !important;
        width: 0 !important;
        height: 0 !important;
        border-radius: 50% !important;
        background: rgba(255, 255, 255, 0.2) !important;
        transform: translate(-50%, -50%) !important;
        transition: width 0.6s, height 0.6s !important;
    }
    
    .primary-button:hover::before {
        width: 300px !important;
        height: 300px !important;
    }
    
    .primary-button:hover {
        transform: translateY(-2px) !important;
        box-shadow: var(--shadow-lg) !important;
    }
    
    .secondary-button, button[variant="secondary"] {
        background: white !important;
        color: var(--neutral-700) !important;
        border: 2px solid var(--neutral-300) !important;
        border-radius: 0.75rem !important;
        padding: 1rem 2rem !important;
        font-weight: 600 !important;
    }
    
    .secondary-button:hover {
        border-color: var(--primary-color) !important;
        color: var(--primary-color) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Sliders */
    input[type="range"] {
        -webkit-appearance: none !important;
        appearance: none !important;
        background: var(--neutral-200) !important;
        height: 6px !important;
        border-radius: 3px !important;
    }
    
    input[type="range"]::-webkit-slider-thumb {
        -webkit-appearance: none !important;
        appearance: none !important;
        width: 20px !important;
        height: 20px !important;
        border-radius: 50% !important;
        background: var(--primary-color) !important;
        cursor: pointer !important;
        box-shadow: var(--shadow-md) !important;
    }
    
    input[type="range"]::-moz-range-thumb {
        width: 20px !important;
        height: 20px !important;
        border-radius: 50% !important;
        background: var(--primary-color) !important;
        cursor: pointer !important;
        box-shadow: var(--shadow-md) !important;
        border: none !important;
    }
    
    /* Accordion */
    .accordion {
        background: white !important;
        border-radius: 1rem !important;
        border: 1px solid var(--neutral-200) !important;
        margin-top: 1.5rem !important;
        overflow: hidden !important;
    }
    
    /* Gallery */
    [data-testid="gallery"] {
        background: white !important;
        border-radius: 1.5rem !important;
        padding: 1.5rem !important;
        box-shadow: var(--shadow-lg) !important;
    }
    
    .gallery-item {
        border-radius: 1rem !important;
        overflow: hidden !important;
        transition: transform 0.3s ease !important;
    }
    
    .gallery-item:hover {
        transform: scale(1.05) !important;
        box-shadow: var(--shadow-xl) !important;
    }
    
    /* Status Text */
    textarea, input[type="text"] {
        border-radius: 0.75rem !important;
        border: 1px solid var(--neutral-200) !important;
        padding: 1rem !important;
        font-size: 0.95rem !important;
        background: var(--neutral-50) !important;
    }
    
    /* Tips Section */
    .tips-section {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%) !important;
        border-radius: 1.5rem !important;
        padding: 3rem !important;
        margin-top: 4rem !important;
        border: 1px solid var(--neutral-200) !important;
    }
    
    .tips-section h3 {
        font-family: 'Playfair Display', serif !important;
        color: var(--neutral-900) !important;
        font-size: 1.75rem !important;
        margin-bottom: 1.5rem !important;
    }
    
    .tips-section ul {
        list-style: none !important;
        padding-left: 0 !important;
    }
    
    .tips-section li {
        padding-left: 2rem !important;
        position: relative !important;
        margin-bottom: 1rem !important;
        color: var(--neutral-700) !important;
        line-height: 1.6 !important;
    }
    
    .tips-section li::before {
        content: '✨' !important;
        position: absolute !important;
        left: 0 !important;
        font-size: 1.2rem !important;
    }
    
    /* Loading Animation */
    @keyframes shimmer {
        0% { background-position: -1000px 0; }
        100% { background-position: 1000px 0; }
    }
    
    .loading {
        background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%) !important;
        background-size: 1000px 100% !important;
        animation: shimmer 2s infinite !important;
    }
    
    /* Footer */
    .footer {
        background: var(--neutral-900) !important;
        color: var(--neutral-300) !important;
        padding: 3rem !important;
        margin-top: 6rem !important;
        text-align: center !important;
        border-radius: 3rem 3rem 0 0 !important;
    }
    
    .footer-text {
        font-size: 0.9rem !important;
        margin-bottom: 1rem !important;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.5rem !important;
        }
        
        .section-header {
            font-size: 2rem !important;
        }
        
        .upload-card {
            padding: 1.5rem !important;
        }
        
        .app-navbar {
            padding: 1rem 1.5rem !important;
        }
    }
    
    /* Smooth Scroll */
    html {
        scroll-behavior: smooth !important;
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 10px !important;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--neutral-100) !important;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary-color) !important;
        border-radius: 5px !important;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--primary-light) !important;
    }
    """
    
    with gr.Blocks(css=custom_css, title="TryOnX - Virtual Fashion Experience", theme=gr.themes.Soft()) as demo:
        
        # Navbar
        with gr.Row(elem_classes="app-navbar"):
            gr.Markdown(
                """
                <div style="display: flex; align-items: center; justify-content: space-between; width: 100%;">
                    <span class="app-logo">✨ TryOnX</span>
                    <div style="display: flex; gap: 2rem; font-size: 0.95rem; color: #57534e;">
                        <span style="cursor: pointer; font-weight: 500;">Home</span>
                        <span style="cursor: pointer; font-weight: 500;">Try On</span>
                        <span style="cursor: pointer; font-weight: 500;">Gallery</span>
                        <span style="cursor: pointer; font-weight: 500;">About</span>
                    </div>
                </div>
                """
            )
        
        # Hero Section
        with gr.Row(elem_classes="hero-section"):
            gr.Markdown(
                """
                <h1 class="hero-title">Experience Fashion Like Never Before</h1>
                <p class="hero-subtitle">Transform the way you shop with AI-powered virtual try-on technology. See yourself in any outfit instantly.</p>
                """
            )
        
        # Main Try-On Section
        gr.Markdown(
            """
            <h2 class="section-header">Virtual Try-On Studio</h2>
            <p class="section-subtitle">Upload your photo and select a garment to see the magic happen</p>
            """,
            elem_classes="main-header"
        )
        
        with gr.Row(equal_height=True):
            # Left column - Inputs
            with gr.Column(scale=1, elem_classes="upload-card"):
                gr.Markdown("### 📸 Your Photo")
                gr.Markdown("<p style='color: #78716c; font-size: 0.9rem; margin-bottom: 1rem;'>Upload a clear, full-body photo facing forward</p>")
                
                model_image = gr.Image(
                    label="Model Image",
                    type="filepath",
                    height=350,
                    elem_classes="upload-section"
                )
            
            # Middle column - Garment
            with gr.Column(scale=1, elem_classes="upload-card"):
                gr.Markdown("### 👗 Garment Selection")
                gr.Markdown("<p style='color: #78716c; font-size: 0.9rem; margin-bottom: 1rem;'>Choose the clothing item you want to try on</p>")
                
                garment_image = gr.Image(
                    label="Garment Image",
                    type="filepath",
                    height=350,
                    elem_classes="upload-section"
                )
            
            # Right column - Results
            with gr.Column(scale=1, elem_classes="upload-card"):
                gr.Markdown("### ✨ Your New Look")
                gr.Markdown("<p style='color: #78716c; font-size: 0.9rem; margin-bottom: 1rem;'>AI-generated result will appear here</p>")
                
                output_gallery = gr.Gallery(
                    label="Generated Look",
                    show_label=False,
                    columns=1,
                    rows=1,
                    height=350,
                    object_fit="contain",
                    elem_classes="gallery"
                )
        
        # Status and Controls
        with gr.Row():
            with gr.Column(scale=3):
                status_text = gr.Textbox(
                    label="Status",
                    interactive=False,
                    placeholder="Ready to transform your look...",
                    show_label=False
                )
            
        # Advanced Settings
        with gr.Row():
            with gr.Column():
                with gr.Accordion("⚙️ Advanced Settings", open=False, elem_classes="accordion"):
                    gr.Markdown("<p style='color: #78716c; font-size: 0.9rem; margin-bottom: 1rem;'>Fine-tune the generation parameters for optimal results</p>")
                    
                    with gr.Row():
                        num_samples = gr.Slider(
                            minimum=1,
                            maximum=4,
                            value=1,
                            step=1,
                            label="🖼️ Number of Variations",
                            info="Generate multiple style options"
                        )
                        
                        num_steps = gr.Slider(
                            minimum=10,
                            maximum=50,
                            value=20,
                            step=1,
                            label="🎯 Quality Steps",
                            info="Higher = Better quality (slower)"
                        )
                    
                    with gr.Row():
                        guidance_scale = gr.Slider(
                            minimum=1.0,
                            maximum=5.0,
                            value=2.0,
                            step=0.1,
                            label="🎨 Style Guidance",
                            info="How closely to match the garment"
                        )
                        
                        seed = gr.Slider(
                            minimum=-1,
                            maximum=999999,
                            value=-1,
                            step=1,
                            label="🎲 Random Seed",
                            info="-1 for random results"
                        )
        
        # Action Buttons
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("<div style='height: 1rem;'></div>")
                generate_btn = gr.Button(
                    "✨ Generate Your Look",
                    variant="primary",
                    size="lg",
                    elem_classes="primary-button"
                )
            with gr.Column(scale=1):
                gr.Markdown("<div style='height: 1rem;'></div>")
                clear_btn = gr.Button(
                    "🔄 Start Over",
                    variant="secondary",
                    size="lg",
                    elem_classes="secondary-button"
                )
        
        # Tips Section
        with gr.Row(elem_classes="tips-section"):
            gr.Markdown(
                """
                <div style="max-width: 1200px; margin: 0 auto;">
                    <h3 style="text-align: center; margin-bottom: 2rem;">💡 Pro Tips for Best Results</h3>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem;">
                        <div>
                            <h4 style="color: #1e40af; margin-bottom: 0.5rem;">📸 Perfect Photo</h4>
                            <ul style="list-style: none; padding-left: 0;">
                                <li>✨ Use clear, well-lit photos</li>
                                <li>✨ Full-body shots work best</li>
                                <li>✨ Face forward in neutral pose</li>
                                <li>✨ Avoid busy backgrounds</li>
                            </ul>
                        </div>
                        <div>
                            <h4 style="color: #10b981; margin-bottom: 0.5rem;">👗 Garment Selection</h4>
                            <ul style="list-style: none; padding-left: 0;">
                                <li>✨ Clean, simple background</li>
                                <li>✨ Garment clearly visible</li>
                                <li>✨ Good lighting and focus</li>
                                <li>✨ Front view preferred</li>
                            </ul>
                        </div>
                        <div>
                            <h4 style="color: #d4af37; margin-bottom: 0.5rem;">⚙️ Settings Guide</h4>
                            <ul style="list-style: none; padding-left: 0;">
                                <li>✨ Start with default settings</li>
                                <li>✨ Increase steps for quality</li>
                                <li>✨ Try different seeds</li>
                                <li>✨ Generate 1 sample first</li>
                            </ul>
                        </div>
                    </div>
                </div>
                """
            )
        
        # About Section
        with gr.Row():
            gr.Markdown(
                """
                <div style="text-align: center; padding: 3rem 2rem; max-width: 800px; margin: 0 auto;">
                    <h3 class="section-header" style="font-size: 2rem;">About TryOnX</h3>
                    <p style="color: #78716c; font-size: 1.1rem; line-height: 1.8; margin-top: 1rem;">
                        Powered by state-of-the-art <strong>OOTDiffusion AI technology</strong>, TryOnX brings the future of fashion to your fingertips. 
                        Our advanced deep learning models understand garment physics, body proportions, and style dynamics to create 
                        photorealistic virtual try-on experiences. Whether you're shopping for tops, dresses, or complete outfits, 
                        TryOnX makes it easy to visualize your perfect look before you buy.
                    </p>
                    <div style="margin-top: 2rem; display: flex; justify-content: center; gap: 1.5rem; flex-wrap: wrap;">
                        <div style="padding: 1rem 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 1rem; font-weight: 600;">
                            🚀 AI-Powered
                        </div>
                        <div style="padding: 1rem 2rem; background: linear-gradient(135deg, #f6d365 0%, #fda085 100%); color: white; border-radius: 1rem; font-weight: 600;">
                            ⚡ Instant Results
                        </div>
                        <div style="padding: 1rem 2rem; background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%); color: white; border-radius: 1rem; font-weight: 600;">
                            🎨 Photorealistic
                        </div>
                    </div>
                </div>
                """
            )
        
        # Footer
        with gr.Row(elem_classes="footer"):
            gr.Markdown(
                """
                <div style="max-width: 1200px; margin: 0 auto;">
                    <p class="footer-text">© 2025 TryOnX. Powered by OOTDiffusion AI Technology.</p>
                    <div style="display: flex; justify-content: center; gap: 2rem; margin-top: 1.5rem; font-size: 1.5rem;">
                        <span style="cursor: pointer;">📧</span>
                        <span style="cursor: pointer;">🐦</span>
                        <span style="cursor: pointer;">📷</span>
                        <span style="cursor: pointer;">💼</span>
                    </div>
                    <p style="margin-top: 1.5rem; font-size: 0.85rem; color: #78716c;">
                        Made with ❤️ for fashion enthusiasts everywhere
                    </p>
                </div>
                """
            )
        
        # Event handlers
        generate_btn.click(
            fn=app.process_tryon,
            inputs=[
                model_image,
                garment_image,
                num_samples,
                num_steps,
                guidance_scale,
                seed
            ],
            outputs=[output_gallery, status_text],
            show_progress="full"  # Show full progress bar
        )
        
        clear_btn.click(
            fn=app.clear_inputs,
            inputs=[],
            outputs=[
                model_image,
                garment_image,
                num_samples,
                num_steps,
                guidance_scale,
                seed,
                output_gallery,
                status_text
            ]
        )
    
    return demo


if __name__ == "__main__":
    # Create and launch the interface
    demo = create_interface()
    
    # Launch with configuration
    demo.launch(
        server_name="127.0.0.1",  # Localhost only
        server_port=7860,         # Default Gradio port
        share=False,              # Set to True to create a public link
        show_error=True,
        inbrowser=True            # Automatically open browser
    )
