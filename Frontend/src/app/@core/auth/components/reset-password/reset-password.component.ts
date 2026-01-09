import { Component, inject } from '@angular/core';
import { FormGroup, Validators } from '@angular/forms';
import { FormBuilder } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { passwordPattern } from '../../../../@shared/common-environment/common-environment';
import { AuthService } from '../../services/auth.service';
import { HttpErrorResponse } from '@angular/common/http';
@Component({
    selector: 'wlk-reset-password',
    templateUrl: './reset-password.component.html',
    styleUrl: './reset-password.component.scss',
    standalone: false
})
export class ResetPasswordComponent {
  hidePassword = true;
  token: string;

  private route = inject(ActivatedRoute);
  private authService = inject(AuthService);
  private router = inject(Router);
  private formBuilder = inject(FormBuilder);

  constructor() {
    this.route.queryParams.subscribe((params) => {
      this.token = params['token'];
    });
  }

  form: FormGroup = this.formBuilder.group({
    password: ['', [Validators.required, Validators.pattern(passwordPattern)]],
    confirmPassword: ['', [Validators.required]],
  }, {
    validators: this.passwordMatchValidator
  });

  private passwordMatchValidator(form: FormGroup) {
    const password = form.get('password');
    const confirmPassword = form.get('confirmPassword');

    if (password?.value !== confirmPassword?.value) {
      confirmPassword?.setErrors({ passwordMismatch: true });
    } else {
      confirmPassword?.setErrors(null);
    }
    return null;
  }

  onSubmit() {
    this.authService.resetPassword(this.token, this.form.value.password).subscribe({
      next: () => {
        this.router.navigate(['/auth/login']);
      },
      error: (error: HttpErrorResponse) => {
        console.log(error);
      }
    });
  }

}
