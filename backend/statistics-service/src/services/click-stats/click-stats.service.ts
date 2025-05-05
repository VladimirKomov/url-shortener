import { Injectable } from '@nestjs/common';
import {ClickEventDto} from "../../dto/click-event.dto";
import {createLogger} from "../../utils/logger.util";

@Injectable()
export class ClickStatsService {
    private readonly logger = createLogger(ClickStatsService.name);

    async handleClickEvent(event: ClickEventDto) {

    }

    async getClickStats() {
        return {
            clicks: 1
        }
    }
}
