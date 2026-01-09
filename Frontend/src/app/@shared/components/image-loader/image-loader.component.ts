import { Component, EventEmitter, Output, signal } from '@angular/core';
import { ImageFile } from '../file-loader/file-loader.component';

@Component({
    selector: 'wlk-image-loader',
    templateUrl: './image-loader.component.html',
    styleUrl: './image-loader.component.scss',
    standalone: false
})
export class ImageLoaderComponent {
  url = signal(undefined);
  @Output() fileChange: EventEmitter<any> = new EventEmitter<ImageFile>();

  constructor() {}

  onFileChange = async (event: any) => {
    const reader = new FileReader();

    if (event.target.files && event.target.files.length) {
      const [file] = event.target.files;

      // Leer el archivo
      reader.readAsDataURL(file);

      reader.onload = async () => {
        const img = new Image();
        img.src = reader.result as string;

        // Esperamos a que la imagen se cargue completamente antes de continuar
        await new Promise((resolve) => {
          img.onload = resolve;
        });

        // Procesar la imagen (redimensionar y comprimir)
        const compressedFile = await this.processImage(img, file);

        // Crear el objeto ImageFile
        const imageFile: ImageFile = {
          file: compressedFile,
          url: URL.createObjectURL(compressedFile),
        };

        // Mostrar la vista previa
        this.url.set(imageFile.url);
        this.fileChange.emit(imageFile);
      };
    }
  };

  // Método de procesamiento de imagen con promesa
  processImage(img: HTMLImageElement, file: File): Promise<File> {
    return new Promise((resolve) => {
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d')!;

      // Define un tamaño máximo, por ejemplo, 1000px
      const maxSize = 800;
      let width = img.width;
      let height = img.height;

      // Redimensionar manteniendo la proporción
      if (width > height && width > maxSize) {
        height = height * (maxSize / width);
        width = maxSize;
      } else if (height > width && height > maxSize) {
        width = width * (maxSize / height);
        height = maxSize;
      }

      // Ajusta el tamaño del canvas
      canvas.width = width;
      canvas.height = height;

      // Dibuja la imagen redimensionada en el canvas
      ctx.drawImage(img, 0, 0, width, height);

      // Comprimir la imagen en formato JPEG con calidad reducida
      canvas.toBlob(
        (blob) => {
          if (blob) {
            const compressedFile = new File([blob], file.name, {
              type: 'image/jpeg',
              lastModified: Date.now(),
            });
            resolve(compressedFile);
          }
        },
        'image/jpeg',
        0.8
      ); // 0.7 es una calidad adecuada para comprimir
    });
  }
}
