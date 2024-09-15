DROP TABLE IF EXISTS public.note;

CREATE TABLE public.note (
    id character varying(32) NOT NULL,
    "replyId" character varying(32),
    "renoteId" character varying(32),
    text text,
    name character varying(256),
    cw character varying(512),
    "userId" character varying(32) NOT NULL,
    "localOnly" boolean DEFAULT false NOT NULL,
    "renoteCount" smallint DEFAULT 0 NOT NULL,
    "repliesCount" smallint DEFAULT 0 NOT NULL,
    reactions jsonb DEFAULT '{}'::jsonb NOT NULL,
    visibility text NOT NULL,
    uri character varying(512),
    "fileIds" character varying(32)[] DEFAULT '{}'::character varying[] NOT NULL,
    "attachedFileTypes" character varying(256)[] DEFAULT '{}'::character varying[] NOT NULL,
    "visibleUserIds" character varying(32)[] DEFAULT '{}'::character varying[] NOT NULL,
    mentions character varying(32)[] DEFAULT '{}'::character varying[] NOT NULL,
    "mentionedRemoteUsers" text DEFAULT '[]'::text NOT NULL,
    emojis character varying(128)[] DEFAULT '{}'::character varying[] NOT NULL,
    tags character varying(128)[] DEFAULT '{}'::character varying[] NOT NULL,
    "hasPoll" boolean DEFAULT false NOT NULL,
    "userHost" character varying(128),
    "replyUserId" character varying(32),
    "replyUserHost" character varying(128),
    "renoteUserId" character varying(32),
    "renoteUserHost" character varying(128),
    url character varying(512),
    "channelId" character varying(32),
    "threadId" character varying(256),
    "reactionAcceptance" character varying(64),
    "clippedCount" smallint DEFAULT '0'::smallint NOT NULL,
    "reactionAndUserPairCache" character varying(1024)[] DEFAULT '{}'::character varying[] NOT NULL
);

INSERT INTO public.note (
    "id",
    "userId",
    "text",
    "cw",
    "visibility",
    "userHost"
    ) VALUES (
        '9kpevjc080',
        '9123nn6mx0',
        'Hello world.',
        '',
        'public',
        null);
