import {ClickEventDto, RawClickEventDto} from "../dto/click-event.dto";

export const mapRawClickEvent = (rawClickEvent: RawClickEventDto): ClickEventDto => {
    return {
        shortCode: rawClickEvent.short_code,
        ipAddress: rawClickEvent.ip_address,
        userAgent: rawClickEvent.user_agent,
        referer: rawClickEvent.referer,
        timestamp: new Date(rawClickEvent.timestamp)
    }
};

