import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ModulesRoutingModule } from './modules-routing.module';
import { IonicModule } from '@ionic/angular';
import { ModulesComponent } from './modules.component';
import { WirtingPage } from './pages/wirting/wirting.page';
import { GrammarPage } from './pages/grammar/grammar.page';
import { HeaderComponent } from './shared/header/header.component';
import { TranslateModule } from '@ngx-translate/core';
import { WritingListComponent } from './shared/writing-list/writing-list.component';
import { ReactiveFormsModule } from '@angular/forms';
import { WritingListResultComponent } from './shared/writing-list-result/writing-list-result.component';


@NgModule({
  declarations: [ModulesComponent, WirtingPage, GrammarPage, HeaderComponent, WritingListComponent, WritingListResultComponent],
  imports: [
    CommonModule,
    IonicModule, // Asegúrate de que esté importado
    ModulesRoutingModule, // Configuración de rutas locales
    TranslateModule,
    ReactiveFormsModule

  ],
  exports: [WirtingPage, GrammarPage, HeaderComponent, WritingListComponent, WritingListResultComponent]
})
export class ModulesModule { }
