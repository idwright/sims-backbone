import { Injectable } from '@angular/core';

import { OAuthService } from 'angular-oauth2-oidc';
import { Configuration } from './typescript-angular-client/configuration';

import { Location } from '@angular/common';

import { ActivatedRoute, UrlSegment } from '@angular/router';
import { Observable } from 'rxjs/Observable';

import { environment } from '../environments/environment';

@Injectable()
export class AuthService {

  accessToken: string;

  constructor(private oauthService: OAuthService, private route:ActivatedRoute, private location: Location ) {
  }

  public getConfiguration() {
    return new Configuration({
      accessToken: this.getAccessToken(),
      basePath: environment.apiLocation,
      withCredentials: false
    });
  }

  public getAccessToken(): string {
      /*
    this.oauthService.silentRefresh().then(info => console.debug('refresh ok', info))
      .catch(err => {
        console.error('refresh error', err);
        this.accessToken = null;
        this.oauthService.logOut();
      });
      */
    this.accessToken = this.oauthService.getAccessToken();
    // console.log("AuthService getAuthToken:" + this.accessToken);
    // console.log(sprocess.env.CLIENT_SECRET);
    return this.accessToken;
  }

}
