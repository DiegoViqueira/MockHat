import { Component, inject, Input, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { finalize } from 'rxjs';
import { AuthService } from 'src/app/@core/auth/services/auth.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss'],
})
export class HeaderComponent implements OnInit {

  private authService = inject(AuthService);

  @Input() title: string = 'MockHat'; // Recibe el título dinámicamente

  constructor(private readonly router: Router) { }

  ngOnInit() {
  }

  logout() {
    this.authService
      .logout()
      .pipe(finalize(() => this.router.navigateByUrl('login')))
      .subscribe();
  }
}
