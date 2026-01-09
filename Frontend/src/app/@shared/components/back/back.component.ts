import { Component, inject, Output, EventEmitter, Input } from '@angular/core';
import { Location } from '@angular/common';
import { Router } from '@angular/router';

@Component({
  selector: 'wlk-back',
  templateUrl: './back.component.html',
  styleUrl: './back.component.scss',
  standalone: false,
})
export class BackComponent {
  private location = inject(Location);
  private router = inject(Router);
  @Output() back = new EventEmitter<void>();
  @Input() url: any = {};
  onBack() {
    this.back.emit();

    if (this.url && this.url.route) {
      this.router.navigate(this.url.route, { queryParams: this.url.queryParams });
    } else {
      this.location.back();
    }

  }
}
