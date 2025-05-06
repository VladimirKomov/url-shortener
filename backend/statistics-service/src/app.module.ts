import {Module} from '@nestjs/common';
import {ConfigModule} from '@nestjs/config';
import {UrlClickConsumer} from "./consumers/url-click.consumer";
import {ClickStatsService} from './services/click-stats/click-stats.service';
import {MongooseModule} from "@nestjs/mongoose";
import {MongoConfigService} from "./database/mongo-config.service";
import {ClickEventEntity, ClickEventSchema} from "./models/click-event.schema";

@Module({
    imports: [
        ConfigModule.forRoot({
            isGlobal: true,
        }),
        MongooseModule.forRootAsync({
            useClass: MongoConfigService,
        }),
        MongooseModule.forFeature([
            {name: ClickEventEntity.name, schema: ClickEventSchema},
        ]),
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
