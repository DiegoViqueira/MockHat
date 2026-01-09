import { Component, Input } from '@angular/core';

@Component({
  selector: 'wlk-progress-bar',
  templateUrl: './progress-bar.component.html',
  styleUrl: './progress-bar.component.scss',
  standalone: false,
})
export class ProgressBarComponent {
  @Input() label: string = '';
  @Input() percentage: number = 0;
}
