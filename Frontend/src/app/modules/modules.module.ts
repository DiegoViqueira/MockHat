import { CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ModulesRoutingModule } from './modules-routing.module';
import { NavigationModule } from './navigation/navigation.module';
import { UsersModule } from './users/users.module';
import { ModulesComponent } from './modules.component';
import { MatRippleModule } from '@angular/material/core';
import { TranslateModule } from '@ngx-translate/core';
import { MatCardModule } from '@angular/material/card';
import { ReactiveFormsModule } from '@angular/forms';
import { PlansModule } from './plans/plans.module';
import { StudentsModule } from './students/students.module';
import { AccountsModule } from './accounts/accounts.module';
@NgModule({
  declarations: [ModulesComponent],
  exports: [
    NavigationModule,
    UsersModule,
    PlansModule,
    StudentsModule,
    AccountsModule
  ],
  imports: [
    CommonModule,
    ModulesRoutingModule,
    NavigationModule,
    UsersModule,
    MatRippleModule,
    TranslateModule,
    MatCardModule,
    ReactiveFormsModule,

  ],
  providers: [],
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
})
export class ModulesModule { }
