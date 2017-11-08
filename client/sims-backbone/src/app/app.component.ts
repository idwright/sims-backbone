import { Component } from '@angular/core';

import { OAuthService } from 'angular-oauth2-oidc';
import { JwksValidationHandler } from 'angular-oauth2-oidc';

import { casAuthConfig } from './auth.config';

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css']
})
export class AppComponent {
    title = 'SIMS Backbone';

    constructor(private oauthService: OAuthService) {

        this.oauthService.configure(casAuthConfig);
        this.oauthService.tokenValidationHandler = new JwksValidationHandler();
    }

    public login() {
        this.oauthService.initImplicitFlow();
    }

    public logout() {
        this.oauthService.logOut();
    }


}
