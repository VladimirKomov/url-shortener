import {Controller, Get, Param, Query} from "@nestjs/common";
import {ClickStatsService} from "../services/click-stats/click-stats.service";
import {createLogger} from "../utils/logger.util";
import {ClickEventResponseDto} from "../dto/click-event.dto";


@Controller('stats')
export class ClickStatsController {
    private readonly logger = createLogger(ClickStatsController.name);

    constructor(private readonly clickStatsService: ClickStatsService) {
    }

    @Get(':shortCode')
    async getClickStats(
        @Param('shortCode') shortCode: string,
        @Query('limit') limit?: string
    ): Promise<ClickEventResponseDto[]> {
        this.logger.log('Get click stats for short code:', shortCode);
        const safeLimit = Math.min(parseInt(limit ?? '100'), 500);
        return this.clickStatsService.getClickStats(shortCode, safeLimit);
    }
}