import { Routes } from '@angular/router';
import { AccountComponent } from '../pages/account/account.component';
import { SignInComponent } from '../pages/sign-in/sign-in.component';
import { SignUpComponent } from '../pages/sign-up/sign-up.component';
import { DashboardsComponent } from '../pages/dashboards/dashboards.component';
import { HomeComponent } from '../pages/home/home.component';
import { SprintsComponent } from '../pages/sprints/sprints.component';
import { TeamsComponent } from '../pages/teams/teams.component';

export const routes: Routes = [
  {
    path: '',
    component: HomeComponent,
    pathMatch: 'full'
  },
  {
    path: 'sprints',
    component: SprintsComponent,
  },
  {
    path: 'dashboards',
    component: DashboardsComponent,
  },
  {
    path: 'teams',
    component: TeamsComponent,
  },
  {
    path: 'sign-in',
    component: SignInComponent,
  },
  {
    path: 'sign-up',
    component: SignUpComponent,
  },
//   {
//     path: 'sign-out',
//     component: SignOutComponent,
//   },
  {
    path: 'account',
    component: AccountComponent,
  },
];