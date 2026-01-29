import { useCurrentFrame, useVideoConfig, interpolate } from "remotion";

export const HelloWorld: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const opacity = interpolate(frame, [0, 30], [0, 1], {
    extrapolateRight: "clamp",
  });

  const translateY = interpolate(frame, [0, 30], [100, 0], {
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        flex: 1,
        textAlign: "center",
        fontSize: "7em",
        backgroundColor: "#1a1a1a",
        color: "white",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        height: "100%",
      }}
    >
      <div
        style={{
          opacity,
          transform: `translateY(${translateY}px)`,
        }}
      >
        Hello World!
      </div>
    </div>
  );
};
