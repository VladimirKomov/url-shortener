import {Controller} from "@nestjs/common";
import {EventPattern, Payload} from "@nestjs/microservices";
import {RawClickEventDto} from "../dto/click-event.dto";
import {mapRawClickEvent} from "../mappers/click-event.mapper";
import {createLogger} from "../utils/logger.util";
import {ClickStatsService} from "../services/click-stats.service";

@Controller()
export class UrlClickConsumer {
    private readonly logger = createLogger(UrlClickConsumer.name);

    constructor(private readonly statsService: ClickStatsService) {}

    @EventPattern('click_events')
    async handleClickEvent(@Payload() rawData: RawClickEventDto) {
        const data = mapRawClickEvent(rawData);
        this.logger.log('Get massage from RabbitMQ:', data.shortCode);
        this.logger.debug(
            'Get massage from RabbitMQ:',
            JSON.stringify(data, null, 2))
        await this.statsService.handleClickEvent(data);
    }
}