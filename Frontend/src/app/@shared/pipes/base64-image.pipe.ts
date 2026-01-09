import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
    name: 'base64Image',
    standalone: false
})
export class Base64ImagePipe implements PipeTransform {
  transform(base64String: string): string {
    return `data:image/png;base64,${base64String}`;
  }
}
