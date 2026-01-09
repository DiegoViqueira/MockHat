import { Component, inject, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { FormBuilder, Validators } from '@angular/forms';
import { MatDialog } from '@angular/material/dialog';
import { LegalDocumentsComponent } from '../legal-documents/legal-documents.component';

@Component({
  selector: 'hrt-login',
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss',
  standalone: false
})
export class LoginComponent implements OnInit {
  dialog = inject(MatDialog);
  hide = true;
  form = this.fb.nonNullable.group({
    Username: ['', [Validators.required, Validators.email]],
    Password: ['', Validators.required],
  });

  year = new Date().getFullYear();

  constructor(
    private readonly fb: FormBuilder,
    private readonly service: AuthService,
    private readonly router: Router,
  ) { }



  login() {
    this.service
      .login(this.form.getRawValue().Username, this.form.getRawValue().Password)
      .subscribe(() => this.router.navigateByUrl('/modules'));
  }

  ngOnInit() {

  }

  clearUrlHash(): void {
    history.replaceState(null, '', window.location.pathname);
  }


  legalDocument(type: string) {
    this.dialog.open(LegalDocumentsComponent, {
      width: '90%',
      maxWidth: '90%',
      data: {
        type: type,
      },
    });
  }

}
