import {Controller} from "@nestjs/common";
import {EventPattern, Payload} from "@nestjs/microservices";
import {ClickEvent} from "./events/click-event.dto";

@Controller()
export class UrlClickConsumer {
    @EventPattern(process.env.RABBITMQ_QUEUE_CLICK_EVENTS || 'click_events')
    async handleClickEvent(@Payload() data: ClickEvent) {
        console.log('Get massage from RabbitMQ:', data);
    }
}