import {Controller} from "@nestjs/common";
import {EventPattern, Payload} from "@nestjs/microservices";
import {RawClickEvent} from "./events/click-event.dto";
import {mapRawClickEvent} from "./mappers/click-event.mapper";

@Controller()
export class UrlClickConsumer {
    @EventPattern(process.env.RABBITMQ_QUEUE_CLICK_EVENTS || 'click_events')
    async handleClickEvent(@Payload() rawData: RawClickEvent) {
        const data = mapRawClickEvent(rawData);
        console.log('Get massage from RabbitMQ:', data);
    }
}