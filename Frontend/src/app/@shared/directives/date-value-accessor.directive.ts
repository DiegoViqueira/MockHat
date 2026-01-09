import {
  Directive,
  ElementRef,
  forwardRef,
  HostListener,
  Provider,
} from '@angular/core';
import { ControlValueAccessor, NG_VALUE_ACCESSOR } from '@angular/forms';

const DATE_VALUE_PROVIDER: Provider = {
  provide: NG_VALUE_ACCESSOR,
  useExisting: forwardRef(() => DateValueAccessorDirective),
  multi: true,
};

@Directive({
    selector: 'input([type=date])[formControlName],input([type=date])[formControl],' +
        'input([type=date])[ngModel]',
    providers: [DATE_VALUE_PROVIDER],
    standalone: false
})
export class DateValueAccessorDirective implements ControlValueAccessor {
  constructor(private element: ElementRef) {}

  @HostListener('input', ['$event.target.valueAsDate'])
  // eslint-disable-next-line @typescript-eslint/ban-types
  private onChange!: Function;

  // eslint-disable-next-line @typescript-eslint/ban-types
  registerOnChange(fn: Function) {
    this.onChange = (valueAsDate: Date) => fn(valueAsDate);
  }

  @HostListener('blur')
  // eslint-disable-next-line @typescript-eslint/ban-types
  private onTouched!: Function;

  // eslint-disable-next-line @typescript-eslint/ban-types
  registerOnTouched(fn: Function) {
    this.onTouched = fn;
  }

  writeValue(date?: Date) {
    this.element.nativeElement.value = this.normalizeValue(date);
  }

  private normalizeValue(date: Date): string {
    return (
      date.getFullYear() +
      '-' +
      ('0' + (date.getMonth() + 1)).slice(-2) +
      '-' +
      ('0' + date.getDate()).slice(-2)
    );
  }
}
