/*
 * Copyright (c) Herta 2023. All Rights Reserved.
 *
 */

import { NgModule } from '@angular/core';
import { AuthRoutingModule } from './auth-routing.module';
import { LoginComponent } from './components/login/login.component';
import { LogoutComponent } from './components/logout/logout.component';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatSelectModule } from '@angular/material/select';
import { MatRadioModule } from '@angular/material/radio';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatDividerModule } from '@angular/material/divider';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatExpansionModule } from '@angular/material/expansion';
import { SharedModule } from '../../@shared/shared.module';
import { MatToolbarModule } from '@angular/material/toolbar';
import { LegalDocumentsComponent } from './components/legal-documents/legal-documents.component';
import { MatDialogActions, MatDialogClose, MatDialogContent } from '@angular/material/dialog';

@NgModule({
  declarations: [LoginComponent, LogoutComponent, LegalDocumentsComponent],
  imports: [
    AuthRoutingModule,
    MatInputModule,
    MatButtonModule,
    MatSelectModule,
    MatRadioModule,
    MatCardModule,
    MatInputModule,
    MatIconModule,
    MatDividerModule,
    MatCheckboxModule,
    MatExpansionModule,
    SharedModule,
    MatToolbarModule,
    MatDialogActions,
    MatDialogContent,
    MatDialogClose,
  ],
})
export class AuthModule {}
