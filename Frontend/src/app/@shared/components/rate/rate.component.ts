import { Component, EventEmitter, Output } from '@angular/core';

@Component({
  selector: 'wlk-rate',
  templateUrl: './rate.component.html',
  styleUrl: './rate.component.scss',
  standalone: false
})
export class RateComponent {
  @Output() onRate: EventEmitter<any> = new EventEmitter<number>();

  rating: number = 0;

  rate(star: number) {
    this.rating = star;
  }
}
