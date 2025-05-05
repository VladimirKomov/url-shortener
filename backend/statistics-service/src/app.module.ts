import {Module} from '@nestjs/common';
import {ConfigModule} from '@nestjs/config';
import {UrlClickConsumer} from "./consumers/url-click.consumer";
import {ClickStatsService} from './services/click-stats/click-stats.service';
import {MongooseModule} from "@nestjs/mongoose";
import {MongoConfigService} from "./database/mongo-config.service";

@Module({
    imports: [
        ConfigModule.forRoot({
            isGlobal: true,
        }),

        MongooseModule.forRootAsync({
            useClass: MongoConfigService,
        }),
    ],
    controllers: [
        UrlClickConsumer,
    ],
    providers: [
        MongoConfigService,
        ClickStatsService
    ],
})
export class AppModule {
}
