import { Directive, ElementRef, forwardRef, HostListener, Provider } from '@angular/core';
import { ControlValueAccessor, NG_VALUE_ACCESSOR } from '@angular/forms';

const DATE_VALUE_PROVIDER: Provider = {
  provide: NG_VALUE_ACCESSOR,
  useExisting: forwardRef(() => DatetimeLocalValueAccessorDirective),
  multi: true,
};

@Directive({
    selector: 'input([type=datetime-local])[formControlName],input([type=datetime-local])[formControl],' +
        'input([type=datetime-local])[ngModel]',
    providers: [DATE_VALUE_PROVIDER],
    standalone: false
})
export class DatetimeLocalValueAccessorDirective implements ControlValueAccessor {
  constructor(private element: ElementRef) {}

  // eslint-disable-next-line @typescript-eslint/ban-types
  private onChange!: Function;

  @HostListener('input', ['$event.target.value']) onInput = (date: string) => {
    this.onChange(new Date(date));
  };

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
    this.element.nativeElement.value = date ? this.normalizeValue(date) : '';
  }

  private normalizeValue(date: Date): string {
    if (isNaN(date.getTime())) return '';

    return (
      date.getFullYear() +
      '-' +
      ('0' + (date.getMonth() + 1)).slice(-2) +
      '-' +
      ('0' + date.getDate()).slice(-2) +
      'T' +
      ('0' + date.getHours()).slice(-2) +
      ':' +
      ('0' + date.getMinutes()).slice(-2) +
      ':' +
      ('0' + date.getSeconds()).slice(-2)
    );
  }
}
