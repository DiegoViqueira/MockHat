
import { NgModule } from '@angular/core';
import { MiscellaneousRoutingModule } from './miscellaneous-routing.module';
import { MiscellaneousComponent } from './miscellaneous.component';
import { NotFoundComponent } from './not-found/not-found.component';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';

@NgModule({
  imports: [
    MiscellaneousRoutingModule,
    CommonModule,
    MatCardModule,
    MatButtonModule,
  ],
  declarations: [MiscellaneousComponent, NotFoundComponent],
})
export class MiscellaneousModule {}
