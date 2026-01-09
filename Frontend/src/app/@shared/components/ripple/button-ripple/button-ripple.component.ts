import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
    selector: 'wlk-button-ripple',
    templateUrl: './button-ripple.component.html',
    styleUrl: './button-ripple.component.scss',
    standalone: false
})
export class ButtonRippleComponent {
  @Input() name: string;
  @Input() icon: string;
  @Input() url: string;

  @Output() emit = new EventEmitter<string>();
  trigger() {
    this.emit.emit(this.url);
  }
}
