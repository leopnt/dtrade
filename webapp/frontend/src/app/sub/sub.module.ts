import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { SubRoutingModule } from './sub-routing.module';
import { SlayoutComponent } from './slayout/slayout.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { SettingsComponent } from './settings/settings.component';
import { SubHeaderComponent } from './sub-header/sub-header.component';
import { FormsModule } from '@angular/forms';


@NgModule({
  declarations: [
    SlayoutComponent,
    DashboardComponent,
    SettingsComponent,
    SubHeaderComponent
  ],
  imports: [
    CommonModule,
    SubRoutingModule,
    FormsModule
  ]
})
export class SubModule { }
