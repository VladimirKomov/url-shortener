import {Controller} from "@nestjs/common";
import {EventPattern, Payload} from "@nestjs/microservices";
import {RawClickEventDto} from "../dto/click-event.dto";
import {mapRawClickEvent} from "../mappers/click-event.mapper";
import {createLogger} from "../utils/logger.util";

@Controller()
export class UrlClickConsumer {
    private readonly logger = createLogger(UrlClickConsumer.name);

    @EventPattern(process.env.RABBITMQ_QUEUE_CLICK_EVENTS || 'click_events')
    async handleClickEvent(@Payload() rawData: RawClickEventDto) {
        const data = mapRawClickEvent(rawData);
        this.logger.log('Get massage from RabbitMQ:', data.shortCode);
        this.logger.debug(
            'Get massage from RabbitMQ:',
            JSON.stringify(data, null, 2))
    }
}