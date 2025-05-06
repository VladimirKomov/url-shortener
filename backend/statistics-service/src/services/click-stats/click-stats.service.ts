import { Injectable } from '@nestjs/common';
import {ClickEventDto, ClickEventResponseDto} from "../../dto/click-event.dto";
import {createLogger} from "../../utils/logger.util";
import {InjectModel} from "@nestjs/mongoose";
import {ClickEventDocument, ClickEventEntity} from "../../models/click-event.schema";
import {Model} from "mongoose";
import {mapClickEventToResponse} from "../../mappers/click-event.mapper";

@Injectable()
export class ClickStatsService {
    private readonly logger = createLogger(ClickStatsService.name);

    constructor(
        @InjectModel(ClickEventEntity.name)
        private readonly clickEventModel: Model<ClickEventDocument>,
    ) {}

    async handleClickEvent(event: ClickEventDto) {
        this.logger.log(`Saving click for shortCode=${event.shortCode}`);

        await this.clickEventModel.create({
            shortCode: event.shortCode,
            ipAddress: event.ipAddress,
            userAgent: event.userAgent,
            referer: event.referer,
            timestamp: event.timestamp || new Date(),
        });
    }

    async getClickStats(shortCode: string): Promise<ClickEventResponseDto[]> {

        const raw = await  this.clickEventModel
            .find({ shortCode })
            .sort({ timestamp: -1 })
            .lean();

        return raw.map(mapClickEventToResponse)
    }
}
