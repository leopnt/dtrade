import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HomeComponent } from './home/home.component';
import { ServiceComponent } from './service/service.component';
import { AboutComponent } from './about/about.component';
import { OffersComponent } from './offers/offers.component';
import { SubscribeComponent } from './subscribe/subscribe.component';
import { PublicRoutingModule } from './public-routing.module';
import { PlayoutComponent } from './playout/playout.component';
import { PheaderComponent } from './pheader/pheader.component';
import { ProcessComponent } from './process/process.component';
import { PfooterComponent } from './pfooter/pfooter.component';



@NgModule({
  declarations: [
    HomeComponent,
    ServiceComponent,
    AboutComponent,
    OffersComponent,
    SubscribeComponent,
    PlayoutComponent,
    PheaderComponent,
    ProcessComponent,
    PfooterComponent
  ],
  imports: [
    CommonModule,
    PublicRoutingModule
  ]
})
export class PublicModule { }
