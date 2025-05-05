export interface RawClickEvent {
    short_code: string;
    ip_address: string;
    user_agent?: string;
    referer?: string;
    timestamp: string;
}

export interface ClickEvent extends Omit<RawClickEvent, 'timestamp'> {
    timestamp: Date;
}