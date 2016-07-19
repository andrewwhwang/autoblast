import Fast5File
import sys

def run(files, end_time=None, group=0, high_quality=False, max_length=-1, min_length=0, normal_quality=False, start_time=None, read_type='all'):

    for fast5 in Fast5File.Fast5FileSet(files, group):

        if start_time or end_time:
            read_start_time = fast5.get_start_time()
            read_end_time = fast5.get_end_time()
        if start_time and start_time > read_start_time:
            fast5.close()
            continue
        if end_time and end_time < read_end_time:
            fast5.close()
            continue

        fas = fast5.get_fastas(read_type)
        # high quality 2D: means there are more nanopore events on the
        # complement strand than on the template strand. We also
        # require there to be a 2D base-called sequence from Metrichor.
        if high_quality:
            if (fast5.get_complement_events_count() <= fast5.get_template_events_count()) or not fast5.has_2D():
                fast5.close()
                continue

        # norem quality 2D : means there are less (or equal) nanopore
        # events on the complement strand than on the template strand.
        # We also require there to be a 2D base-called sequence from Metrichor.
        if normal_quality:
            if (fast5.get_complement_events_count() > fast5.get_template_events_count()) or not fast5.has_2D():
                fast5.close()
                continue

        # with open(args.out_file, 'w') as f:
        #     for fa in fas:
        #         if fa is None or \
        #         len(fa.seq) < min_length or \
        #         (len(fa.seq) > max_length and \
        #         max_length > 0):
        #             continue
        #
        #         f.write("%s\n" % fa)

        fast5.close()
    return fas

# if __name__ == "__main__":
#     print run("../test.fast5")[0]
