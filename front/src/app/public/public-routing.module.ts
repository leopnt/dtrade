import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AboutComponent } from './about/about.component';
import { HomeComponent } from './home/home.component';
import { OffersComponent } from './offers/offers.component';
import { PlayoutComponent } from './playout/playout.component';
import { ServiceComponent } from './service/service.component';
import { SubscribeComponent } from './subscribe/subscribe.component';

const routes: Routes = [

  {
    path: '', component: PlayoutComponent, children: [
      { path: '', redirectTo: 'home', pathMatch: 'full' },

      { path: 'home', component: HomeComponent },
      { path: 'about', component: AboutComponent },
      { path: 'offers', component: OffersComponent },
      { path: 'service', component: ServiceComponent },
      { path: 'subscribe', component: SubscribeComponent }
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class PublicRoutingModule { }
