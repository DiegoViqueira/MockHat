import { Component, EventEmitter, inject, input, Output, signal } from '@angular/core';

export interface ImageFile {
  file: File | undefined;
  url: any | undefined;
}

@Component({
    selector: 'wlk-file-loader',
    templateUrl: './file-loader.component.html',
    styleUrl: './file-loader.component.scss',
    standalone: false
})
export class FileLoaderComponent {
  title = input(undefined);
  url = input(undefined);

  @Output() fileChange: EventEmitter<any> = new EventEmitter<ImageFile>();
  @Output() fileRemoved: EventEmitter<boolean> = new EventEmitter<boolean>();

  remove() {
    this.fileRemoved.emit(true);
  }
  onFileChange(event) {
    const reader = new FileReader();
    if (event.target.files && event.target.files.length) {
      const [file] = event.target.files;

      reader.readAsDataURL(file);
      reader.onload = () => {
        const imageFile: ImageFile = {
          file: file,
          url: reader.result,
        };
        this.fileChange.emit(imageFile);
      };
    }
  }
}
