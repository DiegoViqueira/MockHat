import { Injectable } from '@angular/core';

export interface ImageFile {
    file: File;
    url: string;
}

interface CameraOptions {
    width: number;
    height: number;
    facingMode: 'user' | 'environment'; // 'user' for front camera, 'environment' for back camera
}

@Injectable({
    providedIn: 'root'
})
export class ImageProcessorService {
    private readonly MAX_SIZE = 1024; // Tamaño máximo de la imagen
    private readonly COMPRESSION_QUALITY = 0.8; // Calidad de compresión (0-1)

    /**
     * Procesa un archivo de imagen
     * @param file Archivo de imagen original
     * @returns Promise con el objeto ImageFile procesado
     */

    takePhoto = () => {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();

            reader.onload = async () => {
                const img = new Image();
                img.src = reader.result as string;
            };

        });
    }


    async processImageFiles(files: File[]): Promise<ImageFile[]> {
        return Promise.all(files.map(file => this.processImageFile(file)));
    }


    async processImageFile(file: File): Promise<ImageFile> {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();

            reader.onload = async () => {
                try {
                    const img = new Image();
                    img.src = reader.result as string;

                    // Esperar a que la imagen se cargue
                    await new Promise((res) => {
                        img.onload = res;
                    });

                    // Procesar la imagen
                    const compressedFile = await this.processImage(img, file);

                    const imageFile: ImageFile = {
                        file: compressedFile,
                        url: URL.createObjectURL(compressedFile)
                    };

                    resolve(imageFile);
                } catch (error) {
                    reject(error);
                }
            };

            reader.onerror = () => {
                reject(new Error('Error al leer el archivo'));
            };

            reader.readAsDataURL(file);
        });
    }

    /**
     * Procesa una imagen redimensionándola y comprimiéndola
     * @param img Elemento imagen HTML
     * @param originalFile Archivo original
     * @returns Promise con el archivo procesado
     */
    private processImage(img: HTMLImageElement, originalFile: File): Promise<File> {
        return new Promise((resolve) => {
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d')!;

            // Calcular nuevas dimensiones
            const { width, height } = this.calculateDimensions(img.width, img.height);

            // Configurar canvas
            canvas.width = width;
            canvas.height = height;

            // Dibujar imagen redimensionada
            ctx.drawImage(img, 0, 0, width, height);

            // Comprimir y convertir a archivo
            canvas.toBlob(
                (blob) => {
                    if (blob) {
                        const compressedFile = new File([blob], originalFile.name, {
                            type: 'image/jpeg',
                            lastModified: Date.now()
                        });
                        resolve(compressedFile);
                    }
                },
                'image/jpeg',
                this.COMPRESSION_QUALITY
            );
        });
    }

    /**
     * Calcula las nuevas dimensiones manteniendo la proporción
     * @param width Ancho original
     * @param height Alto original
     * @returns Nuevas dimensiones
     */
    private calculateDimensions(width: number, height: number): { width: number; height: number } {
        if (width > height && width > this.MAX_SIZE) {
            height = height * (this.MAX_SIZE / width);
            width = this.MAX_SIZE;
        } else if (height > width && height > this.MAX_SIZE) {
            width = width * (this.MAX_SIZE / height);
            height = this.MAX_SIZE;
        }

        return { width, height };
    }

    /**
     * Libera los recursos de una URL de objeto
     * @param url URL a liberar
     */
    revokeObjectURL(url: string): void {
        URL.revokeObjectURL(url);
    }

} 