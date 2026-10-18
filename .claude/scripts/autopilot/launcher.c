/* AtlasAutopilot.app launcher.
 *
 * Why: launchd jobs cannot read ~/Documents (macOS TCC) unless the responsible process holds the
 * "Documents folder" grant. A plain python is denied. This tiny signed bundle executable spawns the
 * venv python as a CHILD (not exec), so TCC attributes the child's file access to this app
 * (bundle id ai.iris.atlas.autopilot). Ivo clicks "Allow" once on the first prompt.
 *
 * Usage (from launchd): AtlasAutopilot.app/Contents/MacOS/atlas-autopilot <python> <script> [args...]
 * Built by `meeting_autopilot.py install` (clang + ad-hoc codesign). No logic lives here.
 */
#include <dirent.h>
#include <errno.h>
#include <time.h>
#include <signal.h>
#include <stdlib.h>
#include <spawn.h>
#include <stdio.h>
#include <sys/wait.h>
#include <unistd.h>

extern char **environ;
static pid_t child = 0;

static void forward(int sig) {
    if (child > 0) kill(child, sig);
}

int main(int argc, char **argv) {
    if (argc < 2) {
        fprintf(stderr, "usage: atlas-autopilot <program> [args...]\n");
        return 64;
    }
    /* Touch ~/Documents from this process first: the one-time consent prompt is shown for the app itself. */
    const char *home = getenv("HOME");
    if (home) {
        char path[1024];
        snprintf(path, sizeof path, "%s/Documents/atlas", home);
        DIR *d = opendir(path);
        if (d) {
            closedir(d);
        } else if (errno == EPERM || errno == EACCES) {
            /* No grant yet: tell Ivo once a day how to fix it, then stop (python would fail anyway). */
            char stamp[1100], day[16];
            time_t now = time(NULL);
            strftime(day, sizeof day, "%Y%m%d", localtime(&now));
            snprintf(stamp, sizeof stamp, "%s/Library/Logs/atlas-autopilot/tcc_notified_%s", home, day);
            if (access(stamp, F_OK) != 0) {
                FILE *f = fopen(stamp, "w");
                if (f) fclose(f);
                char *nargv[] = {"/usr/bin/osascript", "-e",
                    "display notification \"System Settings > Privacy & Security > Files and Folders > AtlasAutopilot: turn on Documents\" with title \"Meeting autopilot blocked\"",
                    NULL};
                pid_t p;
                if (posix_spawn(&p, nargv[0], NULL, NULL, nargv, environ) == 0) waitpid(p, NULL, 0);
            }
            fprintf(stderr, "atlas-autopilot: no access to ~/Documents (grant AtlasAutopilot in Files and Folders)\n");
            return 77;
        }
    }
    signal(SIGTERM, forward);
    signal(SIGINT, forward);
    if (posix_spawn(&child, argv[1], NULL, NULL, &argv[1], environ) != 0) {
        perror("posix_spawn");
        return 70;
    }
    int status = 0;
    while (waitpid(child, &status, 0) < 0) {
    }
    return WIFEXITED(status) ? WEXITSTATUS(status) : 128 + WTERMSIG(status);
}
