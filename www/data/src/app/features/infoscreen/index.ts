import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { routes } from './infoscreen.routing';

import { InfoscreenComponent } from './infoscreen.component';


@NgModule({
  imports: [
    CommonModule,
    RouterModule.forChild(routes)
  ],
  declarations: [
    InfoscreenComponent
  ]
})

export class InfoscreenModule {}
