import { Component, inject } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { passwordPattern } from '../../../../@shared/common-environment/common-environment';
import { AuthService } from '../../services/auth.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { HttpErrorResponse } from '@angular/common/http';
import { Router } from '@angular/router';
import { LegalDocumentsComponent } from '../legal-documents/legal-documents.component';
import { MatDialog } from '@angular/material/dialog';

@Component({
  selector: 'wlk-register',
  templateUrl: './register.component.html',
  styleUrl: './register.component.scss',
  standalone: false
})
export class RegisterComponent {

  form: FormGroup;
  hidePassword = true;
  isLoading = false;
  showEmailAlert = false;
  private authService = inject(AuthService);
  private router = inject(Router);
  private dialog = inject(MatDialog);

  constructor(
    private fb: FormBuilder,
    private snackBar: MatSnackBar
  ) {
    this.form = this.fb.group({
      account_name: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      first_name: ['', Validators.required],
      last_name: ['', Validators.required],
      password: ['', [Validators.required, Validators.pattern(passwordPattern)]],
      confirmPassword: ['', Validators.required],
      terms_and_conditions_accepted: [false, Validators.requiredTrue]
    }, {
      validators: this.passwordMatchValidator
    });
  }


  openTermsAndConditionsDialog() {
    this.dialog.open(LegalDocumentsComponent, {
      width: '90%',
      maxWidth: '90%',
    }).afterClosed().subscribe((result: boolean) => {
      if (result) {
        console.log('result', result);
      }
    });
  }

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

  onSubmit(): void {
    if (this.form.valid) {
      this.isLoading = true;
      const formValue = this.form.value;

      this.authService.register(formValue).subscribe({
        next: () => {
          this.isLoading = false;
          this.router.navigate(['/auth/mail-sent']);
        },
        error: (error: HttpErrorResponse) => {
          this.isLoading = false;
          if (error.status === 400) {
            this.snackBar.open(error.error.detail, 'Cerrar', {
              duration: 5000,
              panelClass: ['error-snackbar']
            });
          } else {
            this.snackBar.open('Error en el registro', 'Cerrar', {
              duration: 5000,
              panelClass: ['error-snackbar']
            });
          }
        }
      });
    }
  }

  legalDocument(type: string) {
    this.dialog.open(LegalDocumentsComponent, {
      width: '90%',
      maxWidth: '90%',
      data: { type: type },
    });
  }
}
