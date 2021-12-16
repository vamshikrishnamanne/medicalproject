import { NgModule } from '@angular/core';
import { Routes, RouterModule, ExtraOptions } from '@angular/router';
//
import { HomeComponent } from './home/home.component';
import { StatisticsComponent } from './statistics/statistics.component';
import { HistogramComponent } from './histogram/histogram.component';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';
import { ThresholdSegmentationComponent } from './threshold-segmentation/threshold-segmentation.component';
import { IntensitiesComponent } from './intensities/intensities.component';
import { SnrCnrComponent } from './snr-cnr/snr-cnr.component';

const routes: Routes = [
  { path: 'home', component: HomeComponent, data: { label: 'Home' } },
  { path: 'statistics', component: StatisticsComponent, data: { label: 'Statistics' } },
  { path: 'histogram', component: HistogramComponent, data: { label: 'Histogram' } },
  { path: 'segmentation', component: ThresholdSegmentationComponent, data: { label: 'Segmentation' } },
  { path: 'intensities', component: IntensitiesComponent, data: { label: 'Intensities' } },
  { path: 'snr-cnr', component: SnrCnrComponent, data: { label: 'snr-cnr' } },
  { path: '', redirectTo: 'home', pathMatch: 'full' },
  { path: '**', component: PageNotFoundComponent }
];

const routeOptions: ExtraOptions = {
  enableTracing: true
};

@NgModule({
  imports: [RouterModule.forRoot(routes, routeOptions)],
  exports: [RouterModule]
})
export class AppRoutingModule {}
