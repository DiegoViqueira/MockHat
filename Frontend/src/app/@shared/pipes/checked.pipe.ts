import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
    name: 'checked',
    standalone: false
})
export class CheckedPipe implements PipeTransform {
  transform(value: boolean): string {
    return value ? 'checkmark-outline' : 'close-outline';
  }
}
